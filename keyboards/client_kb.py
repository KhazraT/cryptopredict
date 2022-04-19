from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton('/forecast')

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

# client_keyboard.add(button_1).add(button_2).insert(button_3)
client_keyboard.row(button_1)