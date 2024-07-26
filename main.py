"""
Telegram bot
"""

import os
import random
from collections import defaultdict

import data
import telebot

from bot import init_bot, start_bot



def main():
    """
    Main function
    """
    init_bot()
    preload()
    start_bot()


def preload():
    """
    Load preloaded data
    """
    if "data" not in os.listdir("./"):
        os.mkdir("./data")

    global message_list
    message_list = defaultdict(set)
    global active_users
    active_users = defaultdict(set)

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


def get_mentions(users):
    """
    Get mentions.
    """
    mentions = []
    for i, user in enumerate(users):
        mentions.append(f"{i+1} - [" + user[1] + "](tg://user?id=" + str(user[0]) + ")")
    return mentions


def delete_symb(message):
    """
    Delete useless symbols
    """
    charecters = [
        ",",
        ".",
        "<",
        ">",
        "?",
        ".",
        ";",
        ":",
        "[",
        "]",
        "!",
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
    ]
    for i in charecters:
        message = message.replace(i, "")
    return message


def update_message_list(messages):
    """
    Update messages list
    """
    for message in messages:
        if not message.text.startswith("/"):
            message_text = delete_symb(message.text).lower()
            for i in message_text.split():
                if i != "" and "@" not in i:
                    message_list[message.chat.id].add(i)
                    data.save_data(
                        message_list[message.chat.id], "messages", message.chat.id
                    )


def add_active_users(messages):
    """
    Add active users
    """
    for message in messages:
        if message.from_user.id not in active_users[message.chat.id]:
            active_users[message.chat.id].add(
                (message.from_user.id, message.from_user.first_name)
            )
            data.save_data(active_users[message.chat.id], "users", message.chat.id)


def get_by_id(user_id):
    try:
        user = bot.get_chat(user_id)
        return user.first_name
    except Exception as e:
        pass


def generate_message(message):
    """
    Generate messages
    """
    if "@" not in message.text and random.random() > 0.5:
        message_text = message.text.split()
        message_text[random.randint(0, len(message_text)) - 1] = random.choice(
            list(message_list[message.chat.id])
        )
        message_text = " ".join(message_text)
    else:
        message_len = random.randint(1, min(len(message_list[message.chat.id]), 13))
        message_text = " ".join(
            [
                random.choice(list(message_list[message.chat.id]))
                for _ in range(message_len)
            ]
        )
    if random.random() > 0.8:
        message_text = random_end(message_text)
    if random.random() > 0.90:
        message_text = message_text.upper()
    return message_text


def random_end(message):
    """
    Add random ending
    """
    characters = [
        " :)",
        " :(",
        "..",
        ".",
        "!",
        "?",
        "?!",
        ")))",
        "))",
        ")",
        "(",
        " :+)",
        "!!!",
        "...",
        "?!?!?!",
    ]
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

@bot.message_handler(func=lambda msg: ' чи ' in msg.text and msg.text.lower().startswith("шпак"))
def whether(message):
    options = message.text[5:].split('чи')
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


def get_players_and_choices(message):
    """
    Get players
    """
    players = active_users[message.chat.id]
    if len(players) > 10:
        player_choices = random.sample(sorted(players), 10)
    else:
        player_choices = players
    return players, player_choices

if __name__ =='__main__':
    main()
