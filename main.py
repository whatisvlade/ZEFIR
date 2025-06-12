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
            "georgia": (
                "Грузия — прекрасная страна с горами, морем и вином.",
                "https://example.com/georgia",
                "+375 29 123-45-67"  # Менеджер по Грузии
            ),
            "abkhazia": (
                "Абхазия — отдых на побережье Чёрного моря.",
                "https://example.com/abkhazia",
                "+375 29 234-56-78"
            ),
            "gelendzhik": (
                "Геленджик — курорт на берегу Чёрного моря.",
                "https://example.com/gelendzhik",
                "+375 29 345-67-89"
            ),
            "dagestan": (
                "Дагестан — горы, культура и экстрим.",
                "https://example.com/dagestan",
                "+375 29 456-78-90"
            ),
            "piter": (
                "Питер (Санкт-Петербург) — культурная столица России.",
                "https://example.com/piter",
                "+375 29 567-89-01"
            ),
            "teriberka": (
                "Териберка — север, китов и северное сияние.",
                "https://example.com/teriberka",
                "+375 29 678-90-12"
            ),
            "belarus": (
                "Туры по Беларуси — уют, природа и история.",
                "https://example.com/belarus",
                "+375 29 789-01-23"
            ),
        }
        text, url, manager_phone = tour_links[query.data]
        await query.edit_message_text(
            f"✅ {text}\n\nОзнакомиться подробнее:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Перейти на сайт", url=url)],
                [InlineKeyboardButton("📱 Контакт менеджера направления", url=f"tel:{manager_phone}")],
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
