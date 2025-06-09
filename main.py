import os
import asyncio
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont
import nest_asyncio

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
    keyboard = [
        [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
        [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
        [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
        [InlineKeyboardButton("📞 Связаться", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
        reply_markup=reply_markup
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

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "bus_tours":
        keyboard = [
            [InlineKeyboardButton("🇬🇪 Грузия", callback_data="georgia")],
            [InlineKeyboardButton("🇦🇧 Абхазия", callback_data="abkhazia")],
            [InlineKeyboardButton("🏖️ Геленджик", callback_data="gelendzhik")],
            [InlineKeyboardButton("🌄 Дагестан", callback_data="dagestan")],
            [InlineKeyboardButton("🌉 Питер", callback_data="piter")],
            [InlineKeyboardButton("❄️ Териберка", callback_data="teriberka")],
            [InlineKeyboardButton("🇧🇾 Беларусь", callback_data="belarus")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        await query.edit_message_text("Выберите направление:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "avia_tours":
        await query.edit_message_text(
            "✈️ Авиа туры:\nТут будет информация об авиаперелетах (заглушка)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]])
        )

    elif query.data == "visas":
        await query.edit_message_text(
            "🛂 Визы:\nТут будет информация по визам (заглушка)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]])
        )

    elif query.data == "contact":
        await query.edit_message_text(
            "📞 Связаться:\nТелефон: +375 29 000-00-00\nEmail: info@zefir.travel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]])
        )

    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
            [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
            [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
            [InlineKeyboardButton("📞 Связаться", callback_data="contact")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"Привет, {query.from_user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
            reply_markup=reply_markup
        )

    else:
        await query.edit_message_text(f"Вы выбрали направление: {query.data.upper()}")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))
    application.add_handler(CallbackQueryHandler(handle_button))
    keep_alive()
    await application.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
