"""
Var module
"""

import os
import telebot
from collections import defaultdict

message_list = defaultdict(set)
active_users = defaultdict(set)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
games = {}
set_of_words = set()
