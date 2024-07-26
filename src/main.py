"""
Telegram bot
"""

from bot.chatbot import preload, start_bot


def main():
    """
    Main function
    """
    preload()
    start_bot()


if __name__ == "__main__":
    main()
