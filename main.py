import asyncio
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CONTACT = "+375 29 000-00-00"  # Измени на свой номер!
REQUEST_TRIGGER = "#ЗАЯВКА"            # Слово для поиска в чате

app = Flask('')

@app.route('/')
def home():
    return "✅ Бот работает"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Список стран для виз
visa_countries = [
    ("🇮🇹 Италия", "italy"),
    ("🇪🇸 Испания", "spain"),
    ("🇵🇱 Польша", "poland"),
    ("🇭🇺 Венгрия", "hungary"),
    ("🇫🇷 Франция", "france"),
    ("🇧🇬 Болгария", "bulgaria"),
    ("🇬🇷 Греция", "greece")
]

# Данные автобусных туров
tour_links = {
    "georgia": (
        "Грузия — прекрасная страна с горами, морем и вином.",
        "https://example.com/georgia",
        "+375291234567"
    ),
    "abkhazia": (
        "<b>Абхазия: Два варианта!</b> 1️⃣ <b>АВТОБУСНЫЙ</b> ... 2️⃣ <b>ЖД</b> ... <b>Программы тура:</b> (ссылка кнопкой ниже) ",
        "https://zefirtravel.by/avtobusnie-tury-iz-minska-s-otdyhom-na-more/?set_filter=y&arFilterTours_262_1198337567=Y",
        "+375292345678"
    ),
    "gelendzhik": (
        "<b>Тур в Геленджик</b> <b>Даты:</b> ... <b>Программы тура:</b> (ссылка кнопкой ниже) ",
        "https://zefirtravel.by/avtobusnie-tury-iz-minska-s-otdyhom-na-more/?set_filter=y&arFilterTours_262_2671772459=Y",
        "+375293456789"
    ),
    "dagestan": (
        "<b>Тур в Дагестан</b> Даты: ... ",
        "https://zefirtravel.by/offers/tur-v-dagestan-serdtse-kavkaza/",
        "+375294567890"
    ),
    "piter": (
        "<b>Тур в Санкт-Петербург</b> <b>Даты:</b> ... <b>Программа тура:</b> (ссылка кнопкой ниже) ",
        "https://zefirtravel.by/offers/tur-v-sankt-peterburg-kareliya/",
        "+375295678901"
    ),
    "teriberka": (
        "<b>Тур в Териберку!</b> <b>Даты:</b> ... ",
        "https://zefirtravel.by/offers/teriberka-aysfloating-i-mogushchestvennye-kity/",
        "+375296789012"
    ),
    "belarus": (
        "<b>Западные сокровища Беларуси: Коссово и Ружаны</b> Даты: ... <b>Подробнее:</b> (ссылка кнопкой ниже) ",
        "https://zefirtravel.by/offers/zapadnye-sokrovishcha-belarusi-kossovo-i-ruzhany/",
        "+375297890123"
    ),
}

# Названия направлений
direction_names = {
    "georgia": "Грузия",
    "abkhazia": "Абхазия",
    "gelendzhik": "Геленджик",
    "dagestan": "Дагестан",
    "piter": "Питер",
    "teriberka": "Териберка",
    "belarus": "Беларусь",
    "italy": "Италия",
    "spain": "Испания",
    "poland": "Польша",
    "hungary": "Венгрия",
    "france": "Франция",
    "bulgaria": "Болгария",
    "greece": "Греция"
}

# ---- НОВОЕ: ссылка на самостоятельный подбор тура ----
avia_tour_link = "https://tours.example.com"  # Замените на свою ссылку

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nДобро пожаловать в Zefir Travel!\nВыберите, что вас интересует:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚌 Автобусные туры", callback_data="bus_tours")],
            [InlineKeyboardButton("✈️ Авиа туры", callback_data="avia_tours")],
            [InlineKeyboardButton("🛂 Визы", callback_data="visas")],
            [InlineKeyboardButton("📞 Контакты", callback_data="contact")]
        ])
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # --- Автобусные туры ---
    if query.data == "bus_tours":
        await query.edit_message_text(
            "🚌 Автобусные туры:\nВыберите направление:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌄Грузия", callback_data="georgia")],
                [InlineKeyboardButton("🌄 Абхазия", callback_data="abkhazia")],
                [InlineKeyboardButton("🏖️ Геленджик", callback_data="gelendzhik")],
                [InlineKeyboardButton("🌄 Дагестан", callback_data="dagestan")],
                [InlineKeyboardButton("🌉 Питер", callback_data="piter")],
                [InlineKeyboardButton("❄️ Териберка", callback_data="teriberka")],
                [InlineKeyboardButton("🇧🇾 Беларусь", callback_data="belarus")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    # --- Визы ---
    elif query.data == "visas":
        countries_buttons = [
            [InlineKeyboardButton(flag, callback_data=f"visa_{code}")] for flag, code in visa_countries
        ]
        countries_buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")])
        await query.edit_message_text(
            "🛂 Визы:\nВыберите страну для оформления визы:\n\n"
            f"📱 Контакт менеджера: <code>{MANAGER_CONTACT}</code>",
            reply_markup=InlineKeyboardMarkup(countries_buttons),
            parse_mode="HTML"
        )

    # --- Страница страны по визам ---
    elif query.data.startswith("visa_") and not query.data.startswith("visa_request_"):
        country_code = query.data.replace("visa_", "")
        country = direction_names.get(country_code, country_code)
        await query.edit_message_text(
            f"🛂 <b>Виза в {country}</b>\n\nХотите оставить заявку на визу в {country}?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Оставить заявку", callback_data=f"visa_request_{country_code}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="visas")]
            ]),
            parse_mode="HTML"
        )

    # --- Заявка на визу ---
    elif query.data.startswith("visa_request_"):
        direction = query.data.replace("visa_request_", "")
        title = f"Виза: {direction_names.get(direction, direction)}"
        back_btn = "visas"

        user = query.from_user
        msg = await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"{REQUEST_TRIGGER} {title}\nИмя: {user.first_name} @{user.username if user.username else ''}"
        )

        async def delete_request_msg(bot, chat_id, message_id):
            await asyncio.sleep(3)
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass

        asyncio.create_task(delete_request_msg(context.bot, query.message.chat.id, msg.message_id))

        now_hour = datetime.now().hour
        if 21 <= now_hour or now_hour < 10:
            resp = "Заявка отправлена!\nВ рабочее время с вами свяжется менеджер."
        else:
            resp = "Заявка отправлена!\nОжидайте, с вами свяжется менеджер."

        await query.edit_message_text(
            resp,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data=back_btn)]
            ])
        )

    # --- Страница направления автобусов ---
    elif query.data in tour_links.keys():
        text, url, manager_phone = tour_links[query.data]
        await query.edit_message_text(
            f"{text}\n\n📱 Контакт менеджера: <code>{manager_phone}</code>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Подробнее / Программа тура", url=url)],
                [InlineKeyboardButton("Оставить заявку", callback_data=f"request_{query.data}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="bus_tours")]
            ]),
            parse_mode="HTML"
        )

    # --- Заявка на тур ---
    elif query.data.startswith("request_"):
        direction = query.data.replace("request_", "")
        title = f"Тур: {direction_names.get(direction, direction)}"
        back_btn = "bus_tours"

        user = query.from_user
        msg = await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"{REQUEST_TRIGGER} {title}\nИмя: {user.first_name} @{user.username if user.username else ''}"
        )

        async def delete_request_msg(bot, chat_id, message_id):
            await asyncio.sleep(3)
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass

        asyncio.create_task(delete_request_msg(context.bot, query.message.chat.id, msg.message_id))

        now_hour = datetime.now().hour
        if 21 <= now_hour or now_hour < 10:
            resp = "Заявка отправлена!\nВ рабочее время с вами свяжется менеджер."
        else:
            resp = "Заявка отправлена!\nОжидайте, с вами свяжется менеджер."

        await query.edit_message_text(
            resp,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data=back_btn)]
            ])
        )

    # --- ✈️ Авиа туры: НОВОЕ МЕНЮ ---
    elif query.data == "avia_tours":
        await query.edit_message_text(
            "✈️ Авиа туры:\n\nВыберите действие:",
            f"📱 Контакт менеджера: <code>{MANAGER_CONTACT}</code>",
            reply_markup=InlineKeyboardMarkup(countries_buttons),
            parse_mode="HTML"
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Самостоятельный подбор тура", url=avia_tour_link)],
                [InlineKeyboardButton("Оставить заявку (подбор тура с менеджером)", callback_data="avia_request")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    # --- Оставить заявку (авиа тур, менеджер) ---
    elif query.data == "avia_request":
        user = query.from_user
        msg = await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"{REQUEST_TRIGGER} Авиа тур\nИмя: {user.first_name} @{user.username if user.username else ''}"
        )

        async def delete_request_msg(bot, chat_id, message_id):
            await asyncio.sleep(3)
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass

        asyncio.create_task(delete_request_msg(context.bot, query.message.chat.id, msg.message_id))

        now_hour = datetime.now().hour
        if 21 <= now_hour or now_hour < 10:
            resp = "Заявка на подбор тура отправлена!\nВ рабочее время с вами свяжется менеджер."
        else:
            resp = "Заявка на подбор тура отправлена!\nОжидайте, с вами свяжется менеджер."

        await query.edit_message_text(
            resp,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="avia_tours")]
            ])
        )

    # --- Контакт ---
    elif query.data == "contact":
    await query.edit_message_text(
        f"📞 Контакты:\n"
        f"📱 Менеджер: <code>{MANAGER_CONTACT}</code>\n"
        "🏢 Адрес: г. Минск, ул. Примерная, 1\n"
        "🕓 Время работы: пн-пт 10:00–19:00, сб 11:00–16:00, вс — по договорённости",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]),
        parse_mode="HTML"
    )

    # --- Назад в главное меню ---
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
