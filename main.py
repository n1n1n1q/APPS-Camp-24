"""
Telegram bot
"""

import os
import random
from collections import defaultdict

import data
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

message_list = defaultdict(set)
active_users = defaultdict(set)
questions = data.load_data("data/questions.txt")
polls = {}


def greet_user(messages):
    """
    Greet user
    """
    for message in messages:
        if message.new_chat_members is not None:
            for new_member in message.new_chat_members:
                bot.send_message(message.chat.id, f"Привіт, {new_member.first_name}!")


def get_mentions(users):
    """
    Get mentions.
    """
    mentions = []
    for i, user in enumerate(users):
        mentions.append(f"{i+1} - [" + user[1] + "](tg://user?id=" + str(user[0]) + ")")
    return mentions


def delete_symb(messages):
    """
    Delete useless symbols
    """
    charecters = [
        ",",
        ".",
        "<",
        ">",
        "/",
        "?",
        ".",
        ";",
        ":",
        "[",
        "]",
        "!",
        "@",
        "#",
        "№",
        "$",
        "%",
        "^",
        "*",
        "&",
        "(",
        ")",
        "-",
        "=",
        "+",
        "-",
    ]
    for i in charecters:
        messages = messages.replace(i, "")
    return messages


def update_message_list(messages):
    """
    Update messages list
    """
    for message in messages:
        for i in message.text.split():
            if i != "" or "@" not in i:
                message_list[message.chat.id].add(i)


def add_active_users(messages):
    """
    Add active users
    """
    for message in messages:
        if message.from_user.id not in active_users[message.chat.id]:
            active_users[message.chat.id].add(
                (message.from_user.id, message.from_user.first_name)
            )


def generate_message(message):
    """
    Generate messages
    """
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
            [
                random.choice(list(message_list[message.chat.id]))
                for _ in range(message_len)
            ]
        )
    return message_text


def random_end(message):
    """
    Add random ending
    """
    characters = [":)", ":(", "..", ".", "!", "?", "?!"]
    message += random.choice(characters)
    return message


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
    print(message.text)
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
        ):
            message_text = generate_message(message)
            bot.reply_to(message, message_text)
        if random.random() < 0.01:
            handle_vote(message)


def get_players_and_choices(message):
    """
    Get players
    """
    players = active_users[message.chat.id]
    if len(players) > 10:
        player_choices = random.sample(players, 10)
    else:
        player_choices = players
    print(type(player_choices))
    print(player_choices)
    return players, player_choices


bot.set_update_listener(greet_user)
bot.set_update_listener(update_message_list)
bot.set_update_listener(add_active_users)

bot.infinity_polling()
