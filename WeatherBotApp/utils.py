import requests

from config import State, yandex_maps_api_token, openweather_api_token
from . import db, app
from .models import User, City


def get_current_state(user_id):
    with app.app_context():
        try:
            user = User.query.filter_by(chat_id=user_id).first()
            return user.state
        except Exception as ex:
            return State.S_START


def set_state(user_id, value):
    with app.app_context():
        try:
            user = User.query.filter_by(chat_id=user_id).first()
            user.state = value
            db.session.add(user)
            db.session.commit()
        except:
            user = User(
                chat_id=user_id,
                state=value,
                city_id=1
            )
            db.session.add(user)
            db.session.commit()


def make_request_to_yandex_maps_api(longitude, latitude):
    params = {
        "geocode": f"{longitude}, {latitude}",
        "apikey": yandex_maps_api_token,
        "sco": "longlat",
        "results": 1,
        "kind": "locality",
        "format": "json",
        "lang": "en_RU"
    }

    url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(url, params)
    # print(response.json())
    # with open('response.json', 'w') as jsonfile:
    #     json.dump(response.json(), jsonfile)
    return extract_city_name_from_response(response.json())


def extract_city_name_from_response(response):
    city_name = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
    return city_name


def get_city_id(cityname, longitude, latitude):
    with app.app_context():
        try:
            city = City.query.filter_by(name=cityname.lower()).first()
            return city.id
        except Exception as ex:
            city = City(name=cityname.lower(),
                        longitude=longitude,
                        latitude=latitude)

            db.session.add(city)
            db.session.commit()
            return city.id


def change_city(user_id, cityname, longitude, latitude):
    with app.app_context():
        try:
            user = User.query.filter_by(chat_id=user_id).first()
            user.state = State.S_SEND_NOTIFICATIONS.value
            user.city_id = get_city_id(cityname, longitude, latitude)
        except:
            user = User(
                chat_id=user_id,
                state=State.S_SEND_NOTIFICATIONS.value,
                city_id=get_city_id(cityname, longitude, latitude)
            )
        db.session.add(user)
        db.session.commit()


def get_weather(longitude, latitude):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lon": longitude,
        "lat": latitude,
        "appid": openweather_api_token,
        "units": "metric",
        "mode": "json",
        "cnt": 8,
        "lang": "en"
    }
    print("making request")
    response = requests.get(url, params)
    print(response.text)
    if response.json()['cod'] == "200":
        result = choose_bad_weather(response)
        return result
    else:
        return None


def choose_bad_weather(response):
    bad_weather = []
    data = response.json()
    for elem in data['list']:
        if elem['weather'][0]["main"] not in ["Snow", "Rain"]:
            continue

        report = dict()

        report['time'] = elem['dt_txt']
        report['weather'] = elem['weather'][0]['main']

        bad_weather.append(report)
    return bad_weather


def periodical_weather_checker(bot):
    print('Запуск переодичной задачи')
    with app.app_context():
        cities = City.query.all()
        for city in cities:
            weather_alerts = get_weather(city.longitude, city.latitude)
            if weather_alerts is None:
                text = "Прошу прощения. Не смог найти погоду на сегодня"
            elif len(weather_alerts) == 0:
                text = "Сегодня нет осадков"
            else:
                text = "Осторожно. Сегодня ожидаются осадки:"
                for item in weather_alerts:
                    text += f'\n{item["time"]}: {item["weather"]}'

            for user in city.users:
                if user.state == State.S_SEND_NOTIFICATIONS.value:
                    bot.send_message(user.chat_id, text)