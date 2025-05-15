import telebot
import os
from flask import Flask, request
from datetime import datetime

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

user_states = {}

FACEBOOK_LINK = "https://www.facebook.com/share/12HJtmHryfF/"
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
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # admin কে আলাদা ছবি পাঠানো (forward ছাড়া)
        bot.send_photo(
            ADMIN_CHAT_ID,
            photo=downloaded_file,
            caption=f"নতুন ফলো স্ক্রিনশট\nFrom: @{message.from_user.username or 'N/A'}\nUser ID: {chat_id}"
        )

        user_states[chat_id] = 'verified'
        bot.reply_to(message, "ধন্যবাদ! আমরা আপনার স্ক্রিনশট পেয়েছি এবং ফলো নিশ্চিত করেছি।")
        bot.send_message(chat_id, "আপনার ফলো কনফার্ম হয়েছে, ধন্যবাদ! আপনার লিংক: tg://join?invite=hJOtpJ1_uNBmMWI0 ")
    else:
        bot.reply_to(message, "আপনার ফলো আগেই নিশ্চিত হয়েছে।")

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "OK", 200
    else:
        return "Bot is running", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
