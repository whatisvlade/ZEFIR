import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours"),
            InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")
        ],
        [
            InlineKeyboardButton("📑 Визы", callback_data="visas")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я помогу тебе выбрать тур или оформить визу.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите направление:", reply_markup=reply_markup)

    elif query.data == "main_menu":
        keyboard = [
            [
                InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours"),
                InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")
            ],
            [
                InlineKeyboardButton("📑 Визы", callback_data="visas")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Привет! Я помогу тебе выбрать тур или оформить визу.", reply_markup=reply_markup)

    elif query.data in ["georgia", "abkhazia", "gelendzhik", "dagestan", "piter", "teriberka", "belarus"]:
        text_map = {
            "georgia": "🇬🇪 Грузия",
            "abkhazia": "🇦🇧 Абхазия",
            "gelendzhik": "🏖️ Геленджик",
            "dagestan": "🌄 Дагестан",
            "piter": "🌉 Питер",
            "teriberka": "❄️ Териберка",
            "belarus": "🇧🇾 Беларусь"
        }
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="bus_tours")]]
        await query.edit_message_text(f"Вы выбрали направление: {text_map[query.data]}", reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await query.edit_message_text("Неизвестная команда")

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
