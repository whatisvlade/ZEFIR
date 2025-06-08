from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
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
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
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

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))
    keep_alive()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
