from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask('')

@app.route('/')
def home():
    return "✅ Бот работает"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
            [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
            [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
            [InlineKeyboardButton("📞 Связаться", callback_data="contact")]
        ])
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши любой текст — я превращу его в картинку!")

async def stylize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if user_message is None:
        await update.message.reply_text("Пожалуйста, отправь текст.")
        return

    img = Image.new('RGB', (500, 200), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 90), user_message, font=font, fill=(255, 255, 0))

    img.save('styled_text.png')
    with open('styled_text.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    response_map = {
        "bus_tours": "🚌 Мы предлагаем комфортные автобусные туры по России и Европе.",
        "avia_tours": "✈️ Авиа туры в лучшие направления — подробности на сайте или по телефону.",
        "visas": "🛂 Мы поможем с оформлением виз в Европу и другие страны.",
        "contact": "📞 Связаться с нами: +7 (000) 000-00-00 или @менеджер"
    }

    await query.edit_message_text(response_map.get(query.data, "Выберите один из вариантов ниже."))

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))
    application.add_handler(CallbackQueryHandler(button_handler))
    keep_alive()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

