from aiogram.utils import executor
from handlers import *
from create_bot import *
from config import *
from database import connection

async def on_startup(message: types.Message):
    print("[INFO] Бот был запущен!")
    await bot.send_message(ADMIN, "[INFO] Бот был запущен!")

async def on_shutdown(message: types.Message):
    connection.close()
    await bot.send_message(ADMIN, "[INFO] Бот был выключен!")

regitster_client_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)