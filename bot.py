import telebot
import yt_dlp
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "नमस्ते! मैं एक वीडियो डाउनलोड बॉट हूं।\nकृपया /download भेजें और फिर वीडियो लिंक भेजें।")

@bot.message_handler(commands=['download'])
def ask_for_link(message):
    user_states[message.chat.id] = 'awaiting_link'
    bot.send_message(message.chat.id, "कृपया वीडियो लिंक भेजें (YouTube, Instagram, Facebook)।")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_link')
def handle_video_link(message):
    url = message.text.strip()
    user_states[message.chat.id] = None

    msg = bot.send_message(message.chat.id, "वीडियो प्रोसेस किया जा रहा है... कृपया प्रतीक्षा करें।")

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': f'{message.chat.id}_%(title)s.%(ext)s',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.send_video(message.chat.id, video, caption="यह रहा आपका वीडियो!")

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"त्रुटि हुई: {str(e)}")

bot.infinity_polling()