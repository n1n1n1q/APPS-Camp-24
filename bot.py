import os
import random
import telebot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
games = {}
set_of_words = set()

with open("result_filtered.txt", "r", encoding="UTF-8") as file:
    counter = 0
    for line in file:
        line = line.split(", ")
        if "множина" in line[3]:
            continue
        else:
            if len(line[1]) - 2 == 5:
                counter += 1
                set_of_words.add(line[1][1:-1])
WORDS = list(set_of_words)

@bot.message_handler(commands=['gamble'])
def start_game(message):
    user_id = message.from_user.id
    word = random.choice(WORDS)
    games[user_id] = {"word": word, "attempts": 6, "used_letters": {'correct': [], 'misplaced': [], 'absent': []}}
    with open('photo_start.jpeg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="Привіт, це гра Словко, створена командою Ніч впродовж APPS Summercamp!\nТобі дано 6 спроб, щоб розкрити слово, яке складається з п'яти букв. Успіхів, гра починається!\nВведи своє перше слово:\n Щоб переглянути використані букви, натисни команду /abc")
    games[user_id]["underline"] = ['_', '_', '_', '_', '_']
    games[user_id]["existing_letters"] = []
@bot.message_handler(commands=['abc'])
def abc_ret(message):
    user_id = message.from_user.id
    if user_id in games:
        used_letters = games[user_id]["used_letters"]
        response = "Використані букви:\n"
        response += "Вірно на місці: " + " ".join([f"__{letter}__" for letter in sorted(set(used_letters['correct']), key=lambda x: x[1])]) + "\n"
        response += "Не на своєму місці: " + " ".join([f"*{letter}*" for letter in set(used_letters['misplaced'])])+ "\n"
        response += "Немає в слові: " + " ".join([f"~{letter}~" for letter in set(used_letters['absent'])])
        bot.reply_to(message, response, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Ти не почав гру. Введи команду /gamble щоб почати.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in games:
        return

    text = message.text.lower()
    game = games[user_id]
    word = game["word"]
    if len(text) != len(word):
        bot.reply_to(message, f"Слово має бути з {len(word)} літер.")
        return
    if text not in WORDS:
        bot.reply_to(message, f"Я не знаю такого слова, спробуй ще раз.")
        return 

    if text == word:
        bot.reply_to(message, f"Вітаю! Ви вгадали слово '{word}'!")
        del games[user_id]
        return

    game["attempts"] -= 1

    feedback = generate_feedback(text, word, game["used_letters"], game["underline"], game["existing_letters"])
    bot.reply_to(message, " ".join(feedback))
    bot.reply_to(message, f"Залишилось спроб: {game['attempts']}")
    
    if game["attempts"] == 0:
        bot.reply_to(message, f"Гру закінчено! Слово було '{word}'.")
        del games[user_id]

def generate_feedback(text, word, used_letters, underline, existing_letters):
    feedback = []
    for i in range(len(word)):
        if text[i] == word[i]:
            feedback.append(f"{text[i]} (вірно)\n")
            if text[i] not in used_letters['correct']:
                used_letters['correct'].append((text[i],i+1))
            underline[i] = text[i]
        elif text[i] in word:
            feedback.append(f"{text[i]} (не на своєму місці)\n")
            if text[i] not in used_letters['misplaced']:
                used_letters['misplaced'].append(text[i])
            if text[i] not in existing_letters:
                existing_letters.append(text[i])
        else:
            feedback.append(f"{text[i]} (немає в слові)\n")
            if text[i] not in used_letters['absent']:
                used_letters['absent'].append(text[i])
    return feedback

bot.infinity_polling()
