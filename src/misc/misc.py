"""
Additional functions
"""

import random
import os
from data_process import data
from collections import defaultdict
from data_process.vars import message_list, active_users


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


def generate_feedback(text, word, used_letters, underline, existing_letters):
    feedback = []
    for i in range(len(word)):
        if text[i] == word[i]:
            feedback.append(f"{text[i]} (вірно)\n")
            if text[i] not in used_letters["correct"]:
                used_letters["correct"].append((text[i], i + 1))
            underline[i] = text[i]
        elif text[i] in word:
            feedback.append(f"{text[i]} (не на своєму місці)\n")
            if text[i] not in used_letters["misplaced"]:
                used_letters["misplaced"].append(text[i])
            if text[i] not in existing_letters:
                existing_letters.append(text[i])
        else:
            feedback.append(f"{text[i]} (немає в слові)\n")
            if text[i] not in used_letters["absent"]:
                used_letters["absent"].append(text[i])
    return feedback
