"""
Bot and handlers
"""

import os
import random
from collections import defaultdict

import data
import telebot

from misc import greet_user, update_message_list, add_active_users

def init_bot():
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    global bot
    bot = telebot.TeleBot(BOT_TOKEN)

def start_bot():
    bot.set_update_listener(greet_user)
    bot.set_update_listener(update_message_list)
    bot.set_update_listener(add_active_users)

    bot.infinity_polling()

def greet_user(messages):
    """
    Greet user
    """
    for message in messages:
        if message.new_chat_members is not None:
            for new_member in message.new_chat_members:
                bot.send_message(message.chat.id, f"Привіт, {new_member.first_name}!")
