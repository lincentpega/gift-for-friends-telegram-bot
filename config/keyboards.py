from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

share_button = InlineKeyboardButton('Поделиться', url='https://t.me/Gift_for_friend_test_bot')
start_kb = InlineKeyboardMarkup()
start_kb.add(share_button)

payed_recommendation_button = InlineKeyboardButton('Платная рекомендация', callback_data='start_form')
payed_recommendation_kb = InlineKeyboardMarkup()
payed_recommendation_kb.add(share_button)
payed_recommendation_kb.add(payed_recommendation_button)

try_button = InlineKeyboardButton('Попробовать меня!', callback_data='start_form')
try_kb = InlineKeyboardMarkup()
try_kb.add(share_button)
try_kb.add(try_button)

gift_type_kb = InlineKeyboardMarkup()
gift_type_kb.add(InlineKeyboardButton('Вдумчивый', callback_data='Вдумчивый'))
gift_type_kb.add(InlineKeyboardButton('Сентиментальный', callback_data='Сентиментальный'))
gift_type_kb.add(InlineKeyboardButton('Забавный', callback_data='Забавный'))
gift_type_kb.add(InlineKeyboardButton('Развлекательный', callback_data='Развлекательный'))
gift_type_kb.add(InlineKeyboardButton('Романтичный', callback_data='Романтичный'))

approve_email_kb = InlineKeyboardMarkup()
approve_email_kb.add(InlineKeyboardButton(text='Почта указана верно', callback_data='right_email'))
approve_email_kb.add(InlineKeyboardButton(text='Изменить почту', callback_data='change_email'))
