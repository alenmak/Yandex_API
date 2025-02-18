import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEOCODER_TOKEN = os.getenv('GEOCODER_TOKEN')
STATIC_TOKEN = os.getenv('STATIC_TOKEN')
SEARCH_TOKEN = os.getenv('SEARCH_TOKEN')

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "https://static-maps.yandex.ru/v1"
search_api_server = "https://search-maps.yandex.ru/v1/"


def get_toponym(addr):
    geocoder_params = {
        "apikey": GEOCODER_TOKEN,
        "geocode": addr,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return None
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_toponym_coord(toponym):
    toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates.split(" ")


def get_static_map(**kwargs):  # spn=None, bbox=None, z=None, pt=None):
    map_params = {
        "apikey": STATIC_TOKEN,
    }
    for k, v in kwargs.items():
        if v:
            map_params[k] = v
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print(response.status_code, response.reason)
        return None
    return response.content


def get_spn(toponym):
    lon_lc, lat_lc = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    lon_uc, lat_uc = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    delta = max(abs(lon_uc - lon_lc), abs(lat_uc - lat_lc))
    return ','.join(map(str, (delta, delta)))


def search(text, lang='ru_RU', **kwargs):
    search_params = {
        "apikey": SEARCH_TOKEN,
        "text": text,
        "lang": lang,
    }
    for k, v in kwargs.items():
        if v:
            search_params[k] = v
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(response.status_code, response.reason)
        return None
    return response.json()
