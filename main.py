import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    bot.reply_to(message, "ধন্যবাদ! আমি আপনার বার্তা পেয়েছি।")

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return '', 200
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
