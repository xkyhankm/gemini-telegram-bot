import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

# Render port ayarı için basit Flask sunucusu
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif ve çalışıyor!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# API Anahtarları
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Yapılandırması
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Flask sunucusunu arka planda başlat
    threading.Thread(target=run_flask).start()
    # Telegram botunu başlat
    bot.infinity_polling()