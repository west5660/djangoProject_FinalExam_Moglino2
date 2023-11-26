from telegram import Bot
import logging

logging.basicConfig(level=logging.DEBUG)

def send_telegram_message(chat_id, message_text):
    bot_token = '6148037034:AAGylTPYhWbrZce8J4aCULQF2x7Qns1zv5k'  # Замените на свой токен
    bot = Bot(token=bot_token)
    logging.debug(f"Trying to send message to {chat_id}: {message_text}")
    bot.send_message(chat_id=chat_id, text=message_text)
