"""
Bot and handlers
"""

import os
import random
from collections import defaultdict
import telebot

from misc.misc import (
    update_message_list,
    add_active_users,
    get_players_and_choices,
    get_mentions,
    generate_message,
)
from data_process.vars import message_list, active_users
from data_process import data

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def preload():
    """
    Load preloaded data
    """
    if "data" not in os.listdir("./"):
        os.mkdir("./data")

    for file in os.listdir("data/"):
        if file != "questions.txt":
            data_type, chat_id = file.split("_")
            match data_type:
                case "users":
                    active_users[int(chat_id)] = data.load_data("data/" + file, "users")
                case "chat":
                    message_list[int(chat_id)] = data.load_data(
                        "data/" + file, "messages"
                    )
                case _:
                    raise ValueError(
                        f"Invalid data type! \
        Possible options: users, messages. Got: {data_type}"
                    )
    global questions
    questions = data.load_data("data/questions.txt", "questions")
    global polls
    polls = {}


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


def get_by_id(user_id):
    try:
        user = bot.get_chat(user_id)
        return user.first_name
    except Exception as e:
        pass


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    """
    Send welcome message
    """
    bot.reply_to(
        message,
        'Привіт! Цей бот був зроблений командою "Ніч" протягом APPS Summer Camp 24 ! :)',
    )


@bot.message_handler(commands=["vote"])
def handle_vote(message):
    """
    Handle vote command
    """
    if message.chat.type == "supergroup" or "group":
        _, player_choices = get_players_and_choices(message)
        if len(player_choices) == 1:
            bot.send_message(
                message.chat.id,
                f"Замала кількість активних учасників. Потрібно ще \
{2-len(player_choices)} для створення голосування.",
            )
        else:
            q = random.choice(list(questions))
            msg = f"""{q}
Опції:
{'\n'.join(get_mentions(player_choices))}
"""
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
            bot.send_poll(
                message.chat.id,
                q,
                list(map(str, range(1, len(player_choices) + 1))),
                is_anonymous=False,
            )
    else:
        bot.send_message("Голосування доступне лише в групах")


@bot.message_handler(func=lambda msg: msg.text.lower().startswith("шпак ти"))
def ask_bot(message):
    ans = random.choice(["Так, я", "Ні, я не"])
    bot.reply_to(message, ans + message.text[7:].replace("?", ""))


@bot.message_handler(func=lambda msg: msg.text.lower().startswith("шпак хто"))
def who_is(message):
    users, _ = get_players_and_choices(message)
    user = random.choice(get_mentions(users))
    bot.reply_to(
        message,
        user.split(" - ")[1] + message.text[8:].replace("?", ""),
        parse_mode="Markdown",
    )


@bot.message_handler(
    func=lambda msg: " чи " in msg.text and msg.text.lower().startswith("шпак")
)
def whether(message):
    options = message.text[5:].split("чи")
    bot.reply_to(message, random.choice(options))


@bot.message_handler(func=lambda msg: True)
def randomized_message(message):
    """
    Randomized message generation
    """
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if (
            random.random() > 0.9
            or (
                message.reply_to_message
                and message.reply_to_message.from_user.id == bot.get_me().id
            )
            or bot.get_me().username.lower() in message.text.lower()
            or message.text.lower().startswith("шпак")
        ):
            message_text = generate_message(message)
            bot.reply_to(message, message_text)
        if random.random() < 0.01:
            handle_vote(message)
