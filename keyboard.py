from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_weather = InlineKeyboardButton('Weather', callback_data='weather')
button_wind = InlineKeyboardButton('Wind', callback_data='wind')
button_sun_time = InlineKeyboardButton('Sunrise and Sunset', callback_data='sun_time')
button_currency = InlineKeyboardButton('Currency convert', callback_data='convert')

WEATHER = InlineKeyboardMarkup().add(button_wind, button_sun_time, button_currency)
WIND = InlineKeyboardMarkup().add(button_weather).add(button_sun_time)
SUN_TIME = InlineKeyboardMarkup().add(button_weather, button_wind)
HELP = InlineKeyboardMarkup().add(button_weather, button_wind).add(button_sun_time)
CONVERT = InlineKeyboardMarkup().add(button_currency)


