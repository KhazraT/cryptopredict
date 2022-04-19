from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from predict import get_crypto
from random import uniform
import database
from datetime import datetime

class FSMClient(StatesGroup):
    text = State()

async def start_command(message: types.Message):
    await message.answer("Вы запустили бота\nНажмите на кнопку /forecast, чтобы получить прогноз", reply_markup=client_keyboard)

async def forecast_command(message: types.Message):
    if len(message.text.split()) == 1:
        await FSMClient.text.set()
        await message.reply("Введите название криптовалюты")
    elif len(message.text.split()) == 2:
        name = message.text.split()[1].upper()
        s = get_crypto(name)
        if s != None:
            predict = round(uniform(s*0.95, s*1.05), 2)

            database.insert_into_db(name, predict, datetime.now())
            k = database.get_cpyptoprice(name)

            await message.answer(f"Стоимость на данный момент: {s}")
            await message.answer(f"Прогноз на завтра: {k}")
        else:
            await message.answer("Данной криптовалюты нет в базе данных")
    else:
        await message.answer("Комманда была введена некоректно!")

async def enter_cryptoname(message: types.Message, state: FSMContext):
    if len(message.text.split()) > 1:
        await message.answer("Неправильный формат данных!")
        await state.finish()
    else:
        async with state.proxy() as data:
            data['text'] = message.text.upper()
            s = get_crypto(tuple(data.values())[0])
        if s != None:
            name = message.text.upper()
            predict = round(uniform(s * 0.95, s * 1.05), 2)
            database.insert_into_db(name, predict, datetime.now())
            k = database.get_cpyptoprice(name)

            await message.answer(f"Стоимость на данный момент: {s}")
            await message.answer(f"Прогноз на завтра: {k}")
        else:
            await message.answer("Данной криптовалюты нет в баззе данных")
        await state.finish()

async def echo(message: types.Message):
    await message.answer("Введите команду /forecast и криптовалюту")

def regitster_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['help', 'start'])
    dp.register_message_handler(forecast_command, commands=['forecast'])
    dp.register_message_handler(enter_cryptoname, content_types=['text'], state=FSMClient.text)
    dp.register_message_handler(echo)