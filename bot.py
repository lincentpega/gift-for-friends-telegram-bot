import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, ContentTypes

import sheets
from config import keyboards as kb
from config.env import bot_token, provider_token
from model.user import get_user, add_user, User, mark_user_as_tried

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)

prices = [
    types.LabeledPrice('Рекомендация', 10000)
]


class Form(StatesGroup):
    start = State()
    occasion = State()
    gift_type = State()
    relation = State()
    person_desc = State()
    email = State()
    approve_email = State()
    payment = State()


@dp.callback_query_handler(lambda c: c.data == 'start_form', state=Form.start)
async def start_form(callback: types.CallbackQuery):
    message: types.Message = callback.message
    await Form.occasion.set()
    await bot.edit_message_reply_markup(message.chat.id, message.message_id,
                                        callback.inline_message_id, reply_markup=None)
    await bot.send_message(message.chat.id, 'Какой повод?')


@dp.message_handler(state=[None, Form.start])
async def handle_help(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id

    user = get_user(user_id)
    if user is None:
        user = add_user(User(user_id=user_id, tried=False))

    reply_markup: InlineKeyboardMarkup
    if user.is_tried():
        reply_markup = kb.payed_recommendation_kb
    else:
        reply_markup = kb.try_kb
    await Form.start.set()
    await bot.send_message(user_id,
                           f'Привет {name} !\nМеня зовут Алиса, я бот - помощник стартапа <i>Gift for a friend</i>',
                           reply_markup=reply_markup, parse_mode='HTML')


@dp.message_handler(state=Form.occasion)
async def handle_occasion(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['occasion'] = message.text
    await Form.gift_type.set()
    await bot.send_message(message.chat.id,
                           'Какой тип подарка вы бы хотели?',
                           reply_markup=kb.gift_type_kb)


@dp.callback_query_handler(state=Form.gift_type)
async def handle_gift_type(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['gift_type'] = callback.data
        log.info(f'gift type = {callback.data}')
    await Form.relation.set()
    await bot.send_message(callback.message.chat.id, 'Каково отношение к вам? (например - племянник / босс)')


@dp.message_handler(state=Form.relation)
async def handle_relation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['relation'] = message.text
    await Form.person_desc.set()
    await bot.send_message(message.chat.id,
                           text='Опишите человека в формате :\n'
                                '<code>Это девушка/парень, ей N лет, сейчас он/она занимается___.\n'
                                'Она увлекается __. У него/неё любимый цвет__. Ей приносит радость__.\n'
                                'И в будущем она планирует__.</code>\n'
                                'Если не знаете ответ на какой-либо вопрос, дополните своим',
                           parse_mode='HTML')


@dp.message_handler(state=Form.person_desc)
async def handle_person_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['person_desc'] = message.text
    await Form.email.set()
    await bot.send_message(message.chat.id, 'Поздравляю! Ты прошёл/прошла все вопросы\n'
                                            'Оставь свою почту чтобы мы смогли прислать тебе персональную подборку')


@dp.message_handler(lambda message: is_email_valid(message.text), state=Form.email)
async def handle_correct_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['email'] = message.text
        data['is_payed'] = get_user(message.from_user.id).is_tried()
        await Form.approve_email.set()
        await bot.send_message(message.chat.id, f'Подтвердите правильность почты\n{data["email"]}',
                               reply_markup=kb.approve_email_kb)


@dp.callback_query_handler(lambda c: c.data == 'change_email', state=Form.approve_email)
async def handle_change_email(callback: types.CallbackQuery):
    await Form.email.set()
    await bot.send_message(callback.message.chat.id, 'Введите верную почту')


@dp.callback_query_handler(lambda c: c.data == 'right_email', state=Form.approve_email)
async def handle_right_email(callback: types.CallbackQuery, state: FSMContext):
    await Form.payment.set()
    user = get_user(callback.from_user.id)
    if user.is_tried():
        await bot.send_message(callback.message.chat.id, 'Подарок 🎁- мы также вышлем тебе рекомендации '
                                                'о том как упаковать и преподносить подарок.')
        return await bot.send_invoice(callback.message.chat.id, title='Рекомендации по подарку',
                                      description='Получи персональные рекомендации по подарку',
                                      provider_token=provider_token,
                                      currency='RUB',
                                      prices=prices,
                                      payload='recommendation')
    await Form.start.set()
    mark_user_as_tried(callback.from_user.id)
    await load_data(state)
    return await bot.send_message(callback.message.chat.id,
                                  'Подарок 🎁- мы также вышлем тебе рекомендации '
                                  'о том как упаковать и преподносить подарок.\n'
                                  'Результаты опроса придут тебе на указанную почту в течении двух часов.')


@dp.message_handler(state=Form.approve_email)
@dp.message_handler(lambda message: not is_email_valid(message.text), state=Form.email)
async def handle_incorrect_email(message: types.Message):
    await bot.send_message(message.chat.id, 'Почта неверная, введите ещё раз')


@dp.pre_checkout_query_handler(lambda query: True, state=Form.payment)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message='Что-то пошло не так, попробуйте ещё раз через несколько минут')


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=Form.payment)
async def got_payment(message: types.Message, state: FSMContext):
    await Form.start.set()
    await load_data(state)
    await bot.send_message(message.chat.id, 'Оплата успешно прошла!\n'
                                            'Результаты опроса придут тебе на указанную почту в течении двух часов')


def is_email_valid(email: str) -> int:
    return email.find('@')


async def load_data(state: FSMContext):
    async with state.proxy() as data:
        sheets.append_to_table(
            username=data['username'],
            email=data['email'],
            is_payed=data['is_payed'],
            occasion=data['occasion'],
            gift_type=data['gift_type'],
            relation=data['relation'],
            person_desc=data['person_desc']
        )
