from WeatherBotApp import app, db
from WeatherBotApp.utils import set_state
from WeatherBotApp.models import City

# with app.app_context():
#     # db.drop_all()
#     db.create_all()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4567, debug=False)
