from telebot import TeleBot
import threading
from todo import todo
from notification import notification
import time
import schedule
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN, parse_mode="Markdown")

notification(bot)
todo(bot)


def run_pending():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_pending).start()
    bot.infinity_polling()
