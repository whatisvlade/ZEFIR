import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
        [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
        [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
        [InlineKeyboardButton("📞 Связаться", callback_data="contact")],
    ]
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "bus_tours":
        await query.edit_message_text(
            "🚌 Автобусные туры:
Здесь будет описание автобусных туров.",
            reply_markup=back_button()
        )
    elif query.data == "avia_tours":
        await query.edit_message_text(
            "✈️ Авиа туры:
Здесь будет описание авиа туров.",
            reply_markup=back_button()
        )
    elif query.data == "visas":
        await query.edit_message_text(
            "🛂 Визы:
Здесь будет информация о визах.",
            reply_markup=back_button()
        )
    elif query.data == "contact":
        await query.edit_message_text(
            "📞 Связаться:
Контакты и способы связи с менеджером.",
            reply_markup=back_button()
        )
    elif query.data == "back":
        await start(update, context)

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()