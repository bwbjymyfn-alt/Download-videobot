import os
import time
import telebot
import yt_dlp

TOKEN = '8645779059:AAHmSzVEt-_O3Ut2p8eg1cSaGdArc3HYN38'
ADMIN_ID = 8012687544  

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"أهلاً بك يا {message.from_user.first_name} 🎬⚡\n"
        "أرسل لي رابط أي فيديو وسأقوم بتحميله وإرساله لك فوراً بأعلى سرعة!"
    )

@bot.message_handler(func=lambda message: message.text and (message.text.startswith('http://') or message.text.startswith('https://')))
def download_video(message):
    chat_id = message.chat.id
    url = message.text.strip()
    
    status_msg = bot.send_message(chat_id, "⏳ جاري تحميل الفيديو من السيرفر، يرجى الانتظار...")
    
    unique_id = int(time.time())
    output_filename = f"video_{chat_id}_{unique_id}.mp4"
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'socket_timeout': 30,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        bot.edit_message_text("🚀 تم التحميل! جاري الرفع لك...", chat_id, status_msg.message_id)
        
        with open(output_filename, 'rb') as file:
            bot.send_video(chat_id, file, caption="✅ تم التحميل بواسطة سيرفر البوت السريع!")
            
        bot.delete_message(chat_id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ تعذر تحميل هذا الرابط عبر السيرفر.\nالخطأ: {e}", chat_id, status_msg.message_id)
        
    finally:
        if os.path.exists(output_filename):
            try:
                os.remove(output_filename)
            except:
                pass

print("البوت يعمل أونلاين على السيرفر... 🟢")
bot.infinity_polling(none_stop=True)
