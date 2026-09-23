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
model = genai.GenerativeModel('gemini-3.5-flash-lite')

# Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Uzun mesajları parçalayarak gönderen fonksiyon
def send_long_message(chat_id, text):
    for i in range(0, len(text), 4000):
        bot.send_message(chat_id, text[i:i+4000])

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        # Doğrudan reply_to yerine uzun mesaj desteği sağlayan fonksiyonu çağırıyoruz
        send_long_message(message.chat.id, response.text)
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Flask sunucusunu arka planda başlat
    threading.Thread(target=run_flask).start()
    # Telegram botunu başlat
    bot.infinity_polling()