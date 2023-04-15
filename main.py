from aiogram import executor

from config.db_init import init_db
from bot import dp


if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
