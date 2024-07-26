"""
Bot and handlers
"""

import os
import random
from collections import defaultdict

from misc.misc import (
    update_message_list,
    add_active_users,
    get_players_and_choices,
    get_mentions,
    generate_message,
    generate_feedback,
)
from data_process.vars import message_list, active_users, bot, games, set_of_words
from data_process import data


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
        #         case _:
        #             raise ValueError(
        #                 f"Invalid data type! \
        # Possible options: users, messages. Got: {data_type}"
        #             )

    with open("data/result_filtered.txt", "r", encoding="UTF-8") as file:
        counter = 0
        for line in file:
            line = line.split(", ")
            if "множина" in line[3]:
                continue
            else:
                if len(line[1]) - 2 == 5:
                    counter += 1
                    set_of_words.add(line[1][1:-1])
    global WORDS
    WORDS = list(set_of_words)
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


@bot.message_handler(commands=["gamble"])
def start_game(message):
    user_id = message.from_user.id
    word = random.choice(WORDS)
    games[user_id] = {
        "word": word,
        "attempts": 6,
        "used_letters": {"correct": [], "misplaced": [], "absent": []},
    }
    with open("photo_start.jpeg", "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption="Привіт, це гра Словко, створена командою Ніч впродовж APPS Summercamp!\nТобі дано 6 спроб, щоб розкрити слово, яке складається з п'яти букв. Успіхів, гра починається!\nВведи своє перше слово:\n Щоб переглянути використані букви, натисни команду /abc",
        )
    games[user_id]["underline"] = ["_", "_", "_", "_", "_"]
    games[user_id]["existing_letters"] = []


@bot.message_handler(commands=["abc"])
def abc_ret(message):
    user_id = message.from_user.id
    if user_id in games:
        used_letters = games[user_id]["used_letters"]
        response = "Використані букви:\n"
        response += (
            "Вірно на місці: "
            + " ".join(
                [
                    f"__{letter}__"
                    for letter in sorted(
                        set(used_letters["correct"]), key=lambda x: x[1]
                    )
                ]
            )
            + "\n"
        )
        response += (
            "Не на своєму місці: "
            + " ".join([f"*{letter}*" for letter in set(used_letters["misplaced"])])
            + "\n"
        )
        response += "Немає в слові: " + " ".join(
            [f"~{letter}~" for letter in set(used_letters["absent"])]
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Ти не почав гру. Введи команду /gamble щоб почати.")


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
    if (
        message.chat.type == "group"
        or message.chat.type == "supergroup"
        and message.from_user.id not in games
    ):
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
    else:
        text = message.text.lower()
        game = games[message.from_user.id]
        word = game["word"]
        if len(text) != len(word):
            bot.reply_to(message, f"Слово має бути з {len(word)} літер.")
            return
        if text not in WORDS:
            bot.reply_to(message, f"Я не знаю такого слова, спробуй ще раз.")
            return

        if text == word:
            bot.reply_to(message, f"Вітаю! Ви вгадали слово '{word}'!")
            del games[message.from_user.id]
            return

        game["attempts"] -= 1

        feedback = generate_feedback(
            text,
            word,
            game["used_letters"],
            game["underline"],
            game["existing_letters"],
        )
        bot.reply_to(message, " ".join(feedback))
        bot.reply_to(message, f"Залишилось спроб: {game['attempts']}")

        if game["attempts"] == 0:
            bot.reply_to(message, f"Гру закінчено! Слово було '{word}'.")
            del games[message.from_user.id]
