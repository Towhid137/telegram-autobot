import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

user_states = {}

# আপনার Facebook পেজের লিংক
FACEBOOK_LINK = "https://www.facebook.com/share/12HJtmHryfF/"

# আপনার Telegram ID (যেখানে ছবি ফরওয়ার্ড হবে)
ADMIN_CHAT_ID = 7008410572

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = 'waiting_for_proof'
    bot.send_message(chat_id, f"স্বাগতম!\n\nআমাদের ফেসবুক পেজটি ফলো করুন:\n{FACEBOOK_LINK}\n\nফলো করার পর স্ক্রিনশট পাঠান।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state == 'waiting_for_proof':
        photo = message.photo[-1]
        if photo.file_size > 3000000:
            bot.reply_to(message, "এই ছবিটি অনেক বড় — এটি স্ক্রিনশট নাও হতে পারে। দয়া করে পেজ ফলো করার স্ক্রিনশট দিন।")
            return

        # Admin (আপনার কাছে) স্ক্রিনশট ফরওয়ার্ড করা
        bot.forward_message(ADMIN_CHAT_ID, chat_id, message.message_id)

        user_states[chat_id] = 'verified'
        bot.reply_to(message, "ধন্যবাদ! আমরা আপনার স্ক্রিনশট পেয়েছি এবং ফলো নিশ্চিত করেছি।")
        bot.send_message(chat_id, "আপনার ফলো কনফার্ম হয়েছে, ধন্যবাদ!")
    else:
        bot.reply_to(message, "আপনার ফলো আগেই নিশ্চিত হয়েছে।")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def remind_to_follow(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)

    if state == 'waiting_for_proof':
        bot.send_message(chat_id, f"আপনি এখনো ফলো করেননি বা স্ক্রিনশট দেননি!\n\nফেসবুক পেজটি ফলো করুন:\n{FACEBOOK_LINK}\n\nতারপর স্ক্রিনশট পাঠান।")
    elif state == 'verified':
        bot.send_message(chat_id, "আপনার ফলো ইতিমধ্যেই কনফার্ম হয়েছে। ধন্যবাদ!")

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
