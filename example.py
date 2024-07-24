"""
Example bot
"""

import os
import telebot
import random

BOT_TOKEN = "7317412854:AAF5OSLeKGyPqBMet0GYzNRMBIp5LIGQKnA"
bot = telebot.TeleBot(BOT_TOKEN)

message_list = set()


def greet_user(messages):
    for message in messages:
        if message.new_chat_members:
            for new_member in message.new_chat_members:
                bot.send_message(message.chat.id, f"Привіт, {new_member.first_name}!")


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing?")


@bot.message_handler(func=lambda msg: "привіт" not in msg.text)
def echo_all(message):
    for i in message.text.split():
        if i != "":
            message_list.add(i)
    if random.random() > 5:
        message.text = ""
        # print(random.choices(message_list, random.randint(1, len(message_list))))
        choices_num = random.randint(1, min(len(message_list), 13))
        message.text = " ".join(
            [random.choice(list(message_list)) for _ in range(choices_num)]
        )
        bot.reply_to(message, message.text)
    elif random.random() > 0:
        
        message.text = message.text.split()
        message.text[random.randint(0, len(message.text)) - 1] = random.choice(list(message_list))
        message.text = " ".join(message.text)
        
        bot.reply_to(message, message.text)
        
        # aaa ss ggg
        #     1 
        # [aaa, ss, ggg]
        #      list [ 2 ] = random word
        # reply( ''join(list) )
    
@bot.message_handler(func=lambda msg: "привіт" in msg.text)
def respond_to_hello(message):
    bot.reply_to(message, "привіт!")


bot.set_update_listener(greet_user)

bot.infinity_polling()
