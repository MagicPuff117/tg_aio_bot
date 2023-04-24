from coordinates import get_coordinates
from api_service import get_weather


def weather() -> str:
    wthr = get_weather(get_coordinates())
    return f'{wthr.location}, {wthr.description}\n' \
        f'Temperature is {wthr.temperature} C, feels like {wthr.temperature_feeling} C'


def wind() -> str:
    wthr = get_weather(get_coordinates())
    return f'{wthr.wind_direction} wind, {wthr.wind_speed} m/s'


def sun_time() -> str:
    wthr = get_weather(get_coordinates())
    return f'Sunrise: {wthr.sunrise.strftime("%H:%M")}\n' \
           f'Sunset: {wthr.sunset.strftime("%H:%M")}\n'




