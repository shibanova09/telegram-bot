import json
from lxml import etree
import requests
from conf_reader import config

key_forecast = config.api_forecast.get_secret_value()

def get_location(lat, lon):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    req = requests.get(f'https://nominatim.openstreetmap.org/search.php?q={lat}%2C+{lon}&format=jsonv2&debug=1')
    soup = BeautifulSoup(req.text, 'html.parser')
    t = etree.HTML(str(soup))
    place1 = str(t.xpath('/html/body/pre[10]/text()'))
    place2 = str(t.xpath('/html/body/pre[11]/text()'))
    if len(place1) > len(place2):
        place = place1
    else:
        place = place2
    ind1 = place.index('langaddress')
    ind2 = place.index('placename')
    address = place[ind1 + 17:ind2]
    token = address.split(',')
    city = str(token[2])
    return f'{city}\n{forecast(lat, lon)}'

def forecast(lat, lon):
    url = f'https://api.weather.yandex.ru/v2/informers/?lat={lat}&lon={lon}&[lang=ru_RU]'
    r = requests.get(url, headers={'X-Yandex-API-Key': key_forecast}, verify=False)
    yandex_json = json.loads(r.text)
    print(r)
    conds = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
             'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
             'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
             'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
             'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
             'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
             'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
             }
    wind = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
            'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'
            }
    yandex_json['fact']['condition'] = conds[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind[yandex_json['fact']['wind_dir']]
    for parts in yandex_json['forecast']['parts']:
        parts['condition'] = conds[parts['condition']]
        parts['wind_dir'] = wind[parts['wind_dir']]
    return f'\n{print_forec(yandex_json)}'

def print_forec(yandex_json):
    now = 'Сейчас:' \
          f'\n🌡Температура: {yandex_json["fact"]["temp"]}°C' \
          f'\n🌡Ощущается как: {yandex_json["fact"]["feels_like"]}°C' \
          f'\n☁Облачность/осадки: {yandex_json["fact"]["condition"]}' \
          f'\n💨Скорость ветра: {yandex_json["fact"]["wind_speed"]}м/с' \
          f'\n🧭Направление ветра: {yandex_json["fact"]["wind_dir"]}\n'
    i = 6
    late = ''
    for parts in yandex_json['forecast']['parts']:
        late += f'\nЧерез {str(i)} часов:' \
                f'\n🌡Средняя температура: {parts["temp_avg"]}°C' \
                f'\n🌡Ощущается как: {parts["feels_like"]}°C' \
                f'\n☁Облачность/осадки: {parts["condition"]}' \
                f'\n💨Скорость ветра: {parts["wind_speed"]}м/с' \
                f'\n🧭Направление ветра: {parts["wind_dir"]}\n'
        i += 6
    return now + late