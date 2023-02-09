from apscheduler.schedulers.background import BackgroundScheduler

from config import State
from . import utils


def init_bot(bot):
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(utils.periodical_weather_checker, 'interval', seconds=15, args=[bot])
    scheduler.start()

    @bot.message_handler(commands=['start'])
    def start(message):
        text = """Привет, я бот - предсказатель погоды. """
        bot.send_message(message.chat.id, text)
        try:
            utils.set_state(message.chat.id, State.S_GET_LOCATION.value)
        except Exception as ex:
            print(ex)

    @bot.message_handler(func=lambda message: utils.get_current_state(message.chat.id) == State.S_GET_LOCATION.value,
                         content_types=['location'])
    def get_location_type_location(message):
        try:
            longitude = message.location.longitude
            latitude = message.location.latitude
            bot.send_message(message.chat.id, f'{longitude} / {latitude}')
            city_name = utils.make_request_to_yandex_maps_api(longitude, latitude)
            bot.send_message(message.chat.id, f'Вы находитесь в городе {city_name}')
            utils.get_weather(longitude, latitude)
            utils.change_city(message.chat.id, city_name, longitude, latitude)

        except Exception as ex:
            print(ex)

    @bot.message_handler(func=lambda message: utils.get_current_state(message.chat.id) == State.S_GET_LOCATION,
                         content_types=['text'])
    def get_location_type_location(message):
        try:
            longitude, latitude = message.text.split()
            bot.send_message(message.chat.id, f'{longitude} / {latitude}')
            city_name = utils.make_request_to_yandex_maps_api(longitude, latitude)
            bot.send_message(message.chat.id, f'Вы находитесь в городе {city_name}')
            utils.change_city(message.chat.id, city_name, longitude, latitude)

        except Exception as ex:
            print(ex)
