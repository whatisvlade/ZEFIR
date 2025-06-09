import asyncio
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "bus_tours":
        await query.edit_message_text(
            "🚌 Автобусные туры:\nВыберите направление:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌄🏖️ Грузия", callback_data="georgia")],
                [InlineKeyboardButton("🌄🏖️ Абхазия", callback_data="abkhazia")],
                [InlineKeyboardButton("🏖️ Геленджик", callback_data="gelendzhik")],
                [InlineKeyboardButton("🌄 Дагестан", callback_data="dagestan")],
                [InlineKeyboardButton("🌉 Питер", callback_data="piter")],
                [InlineKeyboardButton("❄️ Териберка", callback_data="teriberka")],
                [InlineKeyboardButton("🇧🇾 Беларусь", callback_data="belarus")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data in ["georgia", "abkhazia", "gelendzhik", "dagestan", "piter", "teriberka", "belarus"]:
        tour_links = {
            "georgia": ("Грузия — прекрасная страна с горами, морем и вином.", "https://example.com/georgia"),
            "abkhazia": ("Абхазия — отдых на побережье Чёрного моря.", "https://example.com/abkhazia"),
            "gelendzhik": ("Геленджик — курорт на берегу Чёрного моря.", "https://example.com/gelendzhik"),
            "dagestan": ("Дагестан — горы, культура и экстрим.", "https://example.com/dagestan"),
            "piter": ("Питер (Санкт-Петербург) — культурная столица России.", "https://example.com/piter"),
            "teriberka": ("Териберка — север, китов и северное сияние.", "https://example.com/teriberka"),
            "belarus": ("Туры по Беларуси — уют, природа и история.", "https://example.com/belarus")
        }
        text, url = tour_links[query.data]
        await query.edit_message_text(
            f"✅ {text}\n\nОзнакомиться подробнее:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Перейти на сайт", url=url)],
                [InlineKeyboardButton("🔙 Назад", callback_data="bus_tours")]
            ])
        )
    elif query.data == "avia_tours":
        await query.edit_message_text(
            "✈️ Авиа туры:\nТут будет информация об авиаперелетах (заглушка)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data == "visas":
        await query.edit_message_text(
            "🛂 Визы:\nТут будет информация по визам (заглушка)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data == "contact":
        await query.edit_message_text(
            "📞 Связаться:\nТелефон: +375 29 000-00-00\nEmail: info@zefir.travel",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data == "back_to_menu":
        await query.edit_message_text(
            f"Привет, {query.from_user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
                [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
                [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
                [InlineKeyboardButton("📞 Связаться", callback_data="contact")]
            ])
        )

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    keep_alive()
    await application.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
