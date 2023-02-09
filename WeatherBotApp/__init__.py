import os

import telebot
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'server.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import bot_processing

bot = telebot.TeleBot(config.token)
bot_processing.init_bot(bot)

from . import views