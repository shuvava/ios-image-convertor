# encoding: utf-8
import ssl
from functools import lru_cache

import geopy

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = context
geolocator = geopy.Nominatim(user_agent='photo_convertor')


@lru_cache(maxsize=1024)
def get_city(latitude: str, longitude: str) -> str:
    """resolve City name by GPS(GEO) coordinates"""
    if latitude == '' or longitude == '':
        return ''
    location = geolocator.reverse(f'{latitude} , {longitude}', timeout=5)
    if location is None:
        return ''
    if 'city' in location.raw['address']:
        city = location.raw['address']['city']
        return city
    elif 'suburb' in location.raw['address']:
        suburb = location.raw['address']['suburb']
        return suburb
    return ''
