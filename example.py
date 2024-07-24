"""
Example bot
"""

import os
import telebot
import random
from collections import defaultdict

BOT_TOKEN = os.environ.get("BOT_TOKEN_EXAMPLE")
bot = telebot.TeleBot(BOT_TOKEN)

message_list = defaultdict(set)
active_users = defaultdict(set)


def greet_user(messages):
    for message in messages:
<<<<<<< HEAD
        for new_member in message.new_chat_members:
            bot.send_message(message.chat.id, f"Привіт, {new_member.first_name}!")
            
def delete_symb(messages):
    charecters = [',', '.','<','>','/','?','.',';',':','[',']','!', '@', '#', '№', '$', '%', '^', '*', '&', '(', ')', '-', '=', '+', '-']
    for i in charecters:
        messages = messages.replace(i, "")
    return messages
=======
        if message.new_chat_members is not None:
            for new_member in message.new_chat_members:
                bot.send_message(message.chat.id, f"Привіт, {new_member.first_name}!")
>>>>>>> 589eb8f (handle vote command)

def update_message_list(messages):
    for message in messages:
        for i in message.text.split():
                if i != "" or "@" not in i:
                    message_list[message.chat.id].add(i)

def add_active_users(messages):
    for message in messages:
        if message.from_user.id not in active_users[message.chat.id]:
            active_users[message.chat.id].add(message.from_user.id)

def generate_message(message):

    if "@" not in message.text and random.random() > 0.5:
        message_text = message.text.split()
        message_text[random.randint(0, len(message_text)) - 1] = random.choice(
            list(message_list[message.chat.id])
        )
        print(message_text)
        message_text = " ".join(message_text)
    else:
        message_len = random.randint(1, min(len(message_list[message.chat.id]), 13))
        message_text = " ".join(
            [random.choice(list(message_list[message.chat.id])) for _ in range(message_len)]
        )
    return message_text

def random_end(message):
    characters = [':)', ':(', "..", '.', "!", "?", "?!"]
    message += random.choice(characters)
    return message

@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Hello!!!!!!!!!!!!!!!!!!!!1!")

@bot.message_handler(commands=["vote"])
def handle_vote(message):
    print(message.text)
    if message.chat.type == "supergroup" or "group":
        players, player_choices = get_players_and_choices(message)
        if message.text == "/vote":
            ...
        else:
            ...
        bot.send_message(message.chat.id, "Vote")
    else:
        bot.send_message("Голосування доступне лише в групах")

@bot.message_handler(func=lambda msg: True)
def randomized_message(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if (
            random.random() > 0.9
            or (
                message.reply_to_message
                and message.reply_to_message.from_user.id == bot.get_me().id
            )
            or bot.get_me().username.lower() in message.text.lower()
        ):
            message_text = generate_message(message)
            bot.reply_to(message, message_text)

@bot.message_handler(func=lambda msg: "привіт" in msg.text)
def respond_to_hello(message):
    bot.reply_to(message, "привіт!")
    

def get_players_and_choices(message):
    players = active_users[message.chat.id]
    if len(players) > 10:
        player_choices = random.sample(players, 10)
    else:
        player_choices = players
    return players, player_choices


bot.set_update_listener(greet_user)
bot.set_update_listener(update_message_list)
bot.set_update_listener(add_active_users)

bot.infinity_polling()
