import os
import telebot
import yt_dlp

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً! أرسل رابط الفيديو للتحميل.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    try:
        ydl_opts = {'format': 'best', 'outtmpl': '%(id)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء التحميل.")

bot.polling()

