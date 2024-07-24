"""
Example bot
"""

import os
import telebot
import pymongo

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

def greet_user(messages):
    for message in messages:
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id, f'Привіт, {new_member.first_name}!')

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing?")

@bot.message_handler(func=lambda msg: "привіт" not in msg.text)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(func=lambda msg: "привіт" in msg.text)
def respond_to_hello(message):
    bot.reply_to(message, "привіт!")

bot.set_update_listener(greet_user)

bot.infinity_polling()
