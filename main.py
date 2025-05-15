import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ইউজার ট্র্যাকিং - কোন ইউজার প্রথম মেসেজ পাঠিয়েছে সেটা মনে রাখার জন্য
user_states = {}

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        user_states[chat_id] = 'waiting_for_photo'
        bot.reply_to(message, "স্বাগতম! দয়া করে একটি ছবি পাঠান।")
    else:
        bot.reply_to(message, "দয়া করে একটি ছবি পাঠান।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == 'waiting_for_photo':
        bot.reply_to(message, "ধন্যবাদ! আমরা আপনার ছবি পেয়েছি।")
        user_states[chat_id] = 'done'
    else:
        bot.reply_to(message, "আপনি আগেই একটি ছবি পাঠিয়েছেন।")

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.stream.read().decode("utf-8")
            )
        ])
        return '', 200
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
