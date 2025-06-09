from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread
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

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
        [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
        [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
        [InlineKeyboardButton("📞 Связаться", callback_data="contact")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Привет, {user.first_name}! 👋\n"
        "Добро пожаловать в Zefir Travel!\n"
        "Выберите, что вас интересует:"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    await query.answer()

    if data == "bus_tours":
        await query.edit_message_text("🚌 Автобусные туры:
(тестовый текст)", reply_markup=back_button())
    elif data == "avia_tours":
        await query.edit_message_text("✈️ Авиа туры:
(тестовый текст)", reply_markup=back_button())
    elif data == "visas":
        await query.edit_message_text("🛂 Визы:
(тестовый текст)", reply_markup=back_button())
    elif data == "contact":
        await query.edit_message_text("📞 Контакты:
(тестовый текст)", reply_markup=back_button())
    elif data == "back":
        await query.edit_message_text(
            f"Привет, {query.from_user.first_name}! 👋\n"
            "Добро пожаловать в Zefir Travel!\n"
            "Выберите, что вас интересует:",
            reply_markup=get_main_menu()
        )

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
    ])

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    keep_alive()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
