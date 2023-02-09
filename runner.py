from WeatherBotApp import app, db
from WeatherBotApp.utils import set_state

with app.app_context():
    db.create_all()
    set_state(1,1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=False)
