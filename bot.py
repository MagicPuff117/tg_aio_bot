import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from urllib.request import urlopen
import config
import keyboard
import messaging



logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




@dp.message_handler(commands=['start', 'weather'])
async def show_weather(message: types.Message):
    await message.answer(text=messaging.weather(),
                         reply_markup=keyboard.WEATHER)


@dp.message_handler(commands='help')
async def show_help_message(message: types.Message):
    await message.answer(
        text=f'This bot can get the current weather from your IP address.',
        reply_markup=keyboard.HELP)


@dp.message_handler(commands='wind')
async def show_wind(message: types.Message):
    await message.answer(text=messaging.wind(),
                         reply_markup=keyboard.WIND)


@dp.message_handler(commands='sun_time')
async def show_sun_time(message: types.Message):
    await message.answer(text=messaging.sun_time(),
                         reply_markup=keyboard.SUN_TIME)


@dp.callback_query_handler(text='weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messaging.weather(),
        reply_markup=keyboard.WEATHER
    )


@dp.callback_query_handler(text='wind')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messaging.wind(),
        reply_markup=keyboard.WIND
    )


@dp.callback_query_handler(text='sun_time')
async def process_callback_sun_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messaging.sun_time(),
        reply_markup=keyboard.SUN_TIME
    )

class SomeState(StatesGroup):
    waiting_for_c1 = State()
    waiting_for_c2 = State()
    waiting_for_amount = State()


async def start_conversion(message: types.Message):
        await message.answer('Please enter the original currency code (e.g. USD)')
        await SomeState.waiting_for_c1.set()


async def get_c1(message: types.Message, state: FSMContext):
        c1 = message.text.upper()
        await message.answer('Please enter the target currency code (e.g. EUR)')
        await state.update_data(c1=c1)
        await SomeState.waiting_for_c2.set()


async def get_c2(message: types.Message, state: FSMContext):
        c2 = message.text.upper()
        await message.answer('Please enter the amount to convert')
        await state.update_data(c2=c2)
        await SomeState.waiting_for_amount.set()


async def get_amount(message: types.Message, state: FSMContext):
    amount = int(message.text)
    data = await state.get_data()
    c1 = data['c1']
    c2 = data['c2']
    response = await convert(c1, c2, amount)
    await message.answer(response)
    await state.finish()

async def convert(c1: str, c2: str, amount: float) -> str:
    url = config.CURRENCY_API.format(c1=c1, c2=c2, amount=amount)
    response = urlopen(url)
    data = json.load(response)
    result = data['result'][c2]
    return result


dp.register_message_handler(start_conversion, commands=['convert'])
dp.register_message_handler(get_c1, state=SomeState.waiting_for_c1)
dp.register_message_handler(get_c2, state=SomeState.waiting_for_c2)
dp.register_message_handler(get_amount, state=SomeState.waiting_for_amount)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)