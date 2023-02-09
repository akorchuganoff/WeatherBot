def init_bot(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        text = """Привет"""
        bot.send_message(message.chat.id, text)
