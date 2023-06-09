from urllib.request import urlopen
from dataclasses import dataclass
import json


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    data = get_url()
    latitude = data['loc'].split(',')[0]
    longitude = data['loc'].split(',')[1]

    return Coordinates(latitude=latitude, longitude=longitude)


def get_url() -> dict:
    url = 'https://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)

