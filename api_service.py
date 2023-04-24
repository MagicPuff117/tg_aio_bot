import json
from typing import TypeAlias, Literal
from enum import IntEnum
from urllib.request import urlopen
from datetime import datetime
from dataclasses import dataclass

import config
from coordinates import Coordinates

Celsius: TypeAlias = float


class WindDirection(IntEnum):
    North = 0
    Northeast = 45
    East = 90
    Southeast = 135
    South = 180
    Southwest = 225
    West = 270
    Northwest = 315

@dataclass(slots=True, frozen=True)
class Weather:
    location: str
    temperature: Celsius
    temperature_feeling: Celsius
    description: str
    wind_speed: float
    wind_direction: str
    sunrise: datetime
    sunset: datetime

def get_weather(coordinates=Coordinates) -> Weather:
    openweather_response = get_response(longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = parse_response(openweather_response)
    return weather


def get_response(latitude: float, longitude: float) -> str:
    url = config.WEATHER_API.format(lat=latitude, lon=longitude)
    return urlopen(url).read()


def parse_response(openweather_response: str) -> Weather:
    openweather_dict = json.loads(openweather_response)
    return Weather(
        location=parse_location(openweather_dict),
        temperature=parse_temperature(openweather_dict),
        temperature_feeling=parse_temperature_feeling(openweather_dict),
        description=parse_description(openweather_dict),
        sunrise=parse_sun_time(openweather_dict, 'sunrise'),
        sunset=parse_sun_time(openweather_dict, 'sunset'),
        wind_speed=parse_wind_speed(openweather_dict),
        wind_direction=parse_wind_direction(openweather_dict)
    )


def parse_location(openweather_dict: dict) -> str:
    return openweather_dict['name']


def parse_temperature(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['temp']

def parse_temperature_feeling(openweather_dict: dict) -> Celsius:
    return openweather_dict['main']['feels_like']

def parse_description(openweather_dict: dict) -> str:
    return str(openweather_dict['weather'][0]['description']).capitalize()

def parse_sun_time(openweather_dict: dict, time: Literal['sunrise', 'sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])

def parse_wind_speed(openweather_dict: dict) -> float:
    return openweather_dict['wind']['speed']

def parse_wind_direction(openweather_dict: dict) -> str:
    degrees = openweather_dict['wind']['deg']
    degrees = round(degrees / 45) * 45
    if degrees == 360:
        degrees = 0
    return WindDirection(degrees).name





