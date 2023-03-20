import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup

import keyboards as kb
from db_init import init_db
from env import bot_token
from user import get_user, add_user, User

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def handle_help(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id

    user = get_user(user_id)
    if user is None:
        user = add_user(User(user_id=user_id, tried=False))

    reply_markup: InlineKeyboardMarkup
    if user.is_tried():
        reply_markup = kb.purchase_kb
    else:
        reply_markup = kb.try_kb

    await message.reply(f'Привет {name} !\nМеня зовут Алиса, я бот - помощник стартапа <i>Gift for a friend</i> - ',
                        reply_markup=reply_markup, parse_mode='html')


@dp.callback_query_handler(text='purchase')
async def handle_purchase(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Purchasing...')


@dp.callback_query_handler(text='try_me')
async def handle_try(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Trying...')


if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
