from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

share_button = InlineKeyboardButton('Поделиться', url='https://google.com')
start_kb = InlineKeyboardMarkup()
start_kb.add(share_button)

purchase_button = InlineKeyboardButton('Оплатить', callback_data='purchase')
purchase_kb = InlineKeyboardMarkup()
purchase_kb.add(share_button)
purchase_kb.add(purchase_button)

try_button = InlineKeyboardButton('Попробовать меня!', callback_data='try_me')
try_kb = InlineKeyboardMarkup()
try_kb.add(share_button)
try_kb.add(try_button)
