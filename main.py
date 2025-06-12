import asyncio
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CONTACT = "+375 29 000-00-00"  # Измени на свой номер!
REQUEST_TRIGGER = "#ЗАЯВКА"            # Триггер-слово для поиска в чате

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
        """<b>Предлагаем два варианта:</b>
1️⃣ <b>АВТОБУСНЫЙ</b>
Едем автобусе туристического класса 🚍
📍 По маршруту: Новополоцк - Полоцк - Минск - Бобруйск - Гомель - Адлер - Цандрипш - Гагра - Гудаута - Новый Афон
⏳ Продолжительность тура: 14 дней, из них 9 ночей отдыхаем на море
🗓 16.06, 20.06, 25.06, 29.06, 04.07, 08.07, 13.07, 17.07, 22.07, 26.07, 31.07, 04.08 и т.д.
💰 от 280$ + 150 BYN

2️⃣ <b>ЖД</b>
Отправляемся на поезде до Адлера 🚝, а далее до Абхазии передвигаемся на туристическом автобусе
📍 По маршруту: Минск - Адлер - Цандрипш - Гагра - Гудаута - Новый Афон
⏳ Продолжительность тура: 15 дней, из них 10 ночей отдыха на море
🗓 18.06, 28.06, 08.07, 18.07, 28.07, 07.08, 17.08, 27.08, 06.09
💰 от 410$ + 150 BYN

<b>Программы тура:</b> (ссылка кнопкой ниже)
""",
        "https://zefirtravel.by/avtobusnie-tury-iz-minska-s-otdyhom-na-more/?set_filter=y&arFilterTours_262_1198337567=Y",
        "+375292345678"
    ),
    "gelendzhik": (
        """<b>Тур в Геленджик</b>
🗓 <b>Даты выезда на 7 ночей:</b>
14.06, 21.06, 28.06, 05.07, 12.07, 19.07, 26.07, 02.08, 09.08, 16.08, 23.08
🗓 <b>Даты выезда на 10 ночей:</b>
13.06, 18.06, 23.06, 28.06, 03.07, 08.07, 13.08, 18.08, 23.08, 28.08, 01.09, 06.09
<b>Программы тура:</b> (ссылка кнопкой ниже)
""",
        "https://zefirtravel.by/avtobusnie-tury-iz-minska-s-otdyhom-na-more/?set_filter=y&arFilterTours_262_2671772459=Y",
        "+375293456789"
    ),
    "dagestan": (
        """<b>Тур в Дагестан: сердце Кавказа!</b>
Подробная программа тура по ссылке (кнопкой ниже)
🚍 Выезжаем из Минска, Могилева и Гомеля на комфортабельном автобусе туристического класса
🗓 <b>Даты выезда:</b> 13.06, 02.07, 12.07, 25.07, 08.08, 22.08, 05.09, 19.09
⏳ <b>Продолжительность тура:</b> 10 дней
💰 <b>Стоимость:</b> 350$ + 150 BYN на человека
""",
        "https://zefirtravel.by/offers/tur-v-dagestan-serdtse-kavkaza/",
        "+375294567890"
    ),
    "piter": (
        """<b>Тур в Санкт-Петербург</b>
Выезжаем на туристическом автобусе и забираем туристов по маршруту:
📍 Гомель - Жлобин - Бобруйск - Минск - Бегомль - Лепель - Полоцк или Витебск - Питер
🗓 <b>Даты выезда:</b> 26.06 и далее каждый четверг!
<b>Программа тура:</b> (ссылка кнопкой ниже)
""",
        "https://zefirtravel.by/offers/tur-v-sankt-peterburg-kareliya/",
        "+375295678901"
    ),
    "teriberka": (
        """<b>Тур в Териберку!</b>
Ознакомиться с полной программой можно по ссылке (кнопкой ниже)
🚍 Выезжаем из Минска, Могилева, Витебска на комфортабельном автобусе туристического класса
🗓 <b>Даты выезда:</b> 03.07, 07.08, 11.09
⏳ <b>Продолжительность тура:</b> 5 дней
💰 <b>Стоимость:</b> 195$ + 100$ на человека
""",
        "https://zefirtravel.by/offers/teriberka-aysfloating-i-mogushchestvennye-kity/",
        "+375296789012"
    ),
    "belarus": (
        """Добрый день! Меня зовут Екатерина — Ваш персональный менеджер ❤️
Вас заинтересовал тур "<b>Западные сокровища Беларуси: Коссово и Ружаны</b>" 😌
🚌 Выезжаем мы из Минска на комфортабельном автобусе
🗓 <b>Даты выезда:</b> 14.06, 28.06, 05.07, 19.07, 02.08, 16.08
⏳ <b>Продолжительность тура:</b> 1 день, выезжаем в 08:00, возвращаемся к 21:00

<b>В туре посетим:</b>
💒 Коссовский замок
🏡 Дом-музей Тадеуша Костюшко
🏛 Дворцовый комплекс рода Сапег в Ружанах
⛪️ Жировичский Свято-Успенский монастырь
🛖 Жировичская купель
💵 <b>Стоимость:</b> 135 BYN на человека

<b>Подробнее:</b> (ссылка кнопкой ниже)
""",
        "https://zefirtravel.by/offers/zapadnye-sokrovishcha-belarusi-kossovo-i-ruzhany/",
        "+375297890123"
    ),
}

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

    # Автобусные туры
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

    elif query.data in tour_links.keys():
        text, url, manager_phone = tour_links[query.data]
        direction_name = {
            "georgia": "Грузия",
            "abkhazia": "Абхазия",
            "gelendzhik": "Геленджик",
            "dagestan": "Дагестан",
            "piter": "Питер",
            "teriberka": "Териберка",
            "belarus": "Беларусь"
        }[query.data]
        await query.edit_message_text(
            f"{text}\n\n📱 Контакт менеджера: <code>{manager_phone}</code>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Подробнее / Программа тура", url=url)],
                [InlineKeyboardButton("Оставить заявку", callback_data=f"request_{query.data}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="bus_tours")]
            ]),
            parse_mode="HTML"
        )

    elif query.data.startswith("request_"):
        direction = query.data.replace("request_", "")
        direction_name = {
            "georgia": "Грузия",
            "abkhazia": "Абхазия",
            "gelendzhik": "Геленджик",
            "dagestan": "Дагестан",
            "piter": "Питер",
            "teriberka": "Териберка",
            "belarus": "Беларусь"
        }.get(direction, direction)
        user = query.from_user
        sent = await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"{REQUEST_TRIGGER} Тур: {direction_name}\nИмя: {user.first_name} @{user.username if user.username else ''}"
        )
        await asyncio.sleep(3)
        try:
            await sent.delete()
        except:
            pass
        now_hour = datetime.now().hour
        if 21 <= now_hour or now_hour < 10:
            resp = "Заявка отправлена!\nВ рабочее время с вами свяжется менеджер."
        else:
            resp = "Заявка отправлена!\nОжидайте, с вами свяжется менеджер."
        await query.edit_message_text(resp, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="bus_tours")]
        ]))

    # Авиа-туры
    elif query.data == "avia_tours":
        await query.edit_message_text(
            "✈️ Авиа туры:\nТут будет информация об авиаперелетах (заглушка)",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    # Визы
    elif query.data == "visas":
        await query.edit_message_text(
            "🛂 Визы:\nВыберите страну:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(flag, callback_data=f"visa_{code}") for flag, code in visa_countries[:4]],
                [InlineKeyboardButton(flag, callback_data=f"visa_{code}") for flag, code in visa_countries[4:]],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data.startswith("visa_"):
        country_code = query.data.replace("visa_", "")
        country_names = {
            "italy": "Италия",
            "spain": "Испания",
            "poland": "Польша",
            "hungary": "Венгрия",
            "france": "Франция",
            "bulgaria": "Болгария",
            "greece": "Греция"
        }
        country = country_names.get(country_code, country_code)
        await query.edit_message_text(
            f"🛂 <b>Виза в {country}</b>\n\n"
            f"📱 Контакт менеджера: <code>{MANAGER_CONTACT}</code>\n\n"
            f"Хотите оставить заявку на визу в {country}?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Оставить заявку", callback_data=f"visa_request_{country_code}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="visas")]
            ]),
            parse_mode="HTML"
        )
    elif query.data.startswith("visa_request_"):
        country_code = query.data.replace("visa_request_", "")
        country_names = {
            "italy": "Италия",
            "spain": "Испания",
            "poland": "Польша",
            "hungary": "Венгрия",
            "france": "Франция",
            "bulgaria": "Болгария",
            "greece": "Греция"
        }
        country = country_names.get(country_code, country_code)
        user = query.from_user
        sent = await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"{REQUEST_TRIGGER} Виза: {country}\nИмя: {user.first_name} @{user.username if user.username else ''}"
        )
        await asyncio.sleep(3)
        try:
            await sent.delete()
        except:
            pass
        now_hour = datetime.now().hour
        if 21 <= now_hour or now_hour < 10:
            resp = "Заявка отправлена!\nВ рабочее время с вами свяжется менеджер."
        else:
            resp = "Заявка отправлена!\nОжидайте, с вами свяжется менеджер."
        await query.edit_message_text(resp, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад", callback_data="visas")]
        ]))

    elif query.data == "contact":
        await query.edit_message_text(
            f"📞 Связаться:\nТелефон: {MANAGER_CONTACT}\nEmail: info@zefir.travel",
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
