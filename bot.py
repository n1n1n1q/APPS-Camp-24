import os
import random
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

games = {}

@bot.message_handler(func=lambda message: message.text.lower().startswith("давай зіграємо"))
def start_game(message):
    user_id = message.from_user.id
    WORDS = [
        ["матір"],["браво"],["кавун"],
        ["місто"],["лікар"],["масло"],
        ["чайка"],["весна"],["осінь"],
        ["іврит"],["хатка"],["садок"],
        ["книга"],["фільм"],["пенал"],
        ["ручка"],["бабця"],["голос"],
        ["ліжко"],["думка"],["жінка"],
        ["гуска"],["качка"],["кишка"],
        ["ринок"],["павич"],["цукор"],
        ["щипці"],["фавор"],["циган"],
        ["олень"],["слина"],["спина"],
        ["дочка"],["обруч"],["школа"],
        ["театр"],["дрова"],["дідок"],
        ["мороз"],["гість"],["вечір"],
        ["канал"],["череп"],["пічка"],
        ["банда"],["зірка"],["камін"],
        ["філія"],["труси"],["зефір"],
        ["гуляш"],["банка"],["ґанок"],
        ["пацюк"],["груша"],["кабан"],
        ["метал"],["салат"],["чобіт"],
        ["їхати"],["нести"],["везти"],
        ["колія"],["геній"],["літак"],
        ["свиня"],["павук"],["індик"],
        ["пісня"],["клоун"],["лінія"],
        ["опера"],["бичок"],["вітер"],
        ["город"],["буряк"],["львів"],
        ["лодзь"],["сюжет"],["подія"],
        ["потік"],["битва"],["буква"],
        ["шахта"],["фірма"],["мітла"],
        ["смуга"],["казка"],["хмара"],
        ["увага"],["листя"],["думка"],
        ["тітка"],["війна"],["бійка"],
        ["група"],["кобра"],["жнива"],
        ["епоха"],["цифра"],["заєць"],
        ["дошка"],["ребро"],["кішка"]
    ]
    word = random.choice(WORDS)
    games[user_id] = {"word": word, "attempts": 6}
    bot.reply_to(message, "Гра почалась! Введи своє перше слово.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.lower()

    if user_id in games:
        game = games[user_id]
        word = game["word"]

        if len(text) != len(word):
            bot.reply_to(message, f"Слово має бути з {len(word)} літер.")
            return

        if text == word:
            bot.reply_to(message, f"Вітаю! Ви вгадали слово '{word}'!")
            del games[user_id]
            return

        game["attempts"] -= 1
        if game["attempts"] == 0:
            bot.reply_to(message, f"Гру закінчено! Слово було '{word}'.")
            del games[user_id]
            return

        feedback = []
        for i in range(len(word)):
            if text[i] == word[i]:
                feedback.append(f"{text[i]} (вірно)")
            elif text[i] in word:
                feedback.append(f"{text[i]} (не на своєму місці)")
            else:
                feedback.append(f"{text[i]} (немає в слові)")
        
        bot.reply_to(message, " ".join(feedback))
        bot.reply_to(message, f"Залишилось спроб: {game['attempts']}")

bot.infinity_polling()
