import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from jinja2 import Template
import zipfile
import shutil
import asyncio
import time
import tempfile

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    name = State()
    email = State()
    password = State()
    emailpassword = State()
    chat_id = State()
    travel_date = State()
    visa_type = State()
    date_range = State()
    forbidden_dates = State()
    strategy = State()

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Введите ФИО:")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите email (логин):")
    await state.set_state(Form.email)

@dp.message(Form.email)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await message.answer("Введите пароль:")
    await state.set_state(Form.password)

@dp.message(Form.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text.strip())
    await message.answer("Введите пароль от почты:")
    await state.set_state(Form.emailpassword)

@dp.message(Form.emailpassword)
async def get_email_password(message: types.Message, state: FSMContext):
    await state.update_data(emailpassword=message.text.strip())
    await message.answer("Введите chat ID:")
    await state.set_state(Form.chat_id)

@dp.message(Form.chat_id)
async def get_chat_id(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.text.strip())
    await message.answer("Введите дату поездки (например 2025-08-01):")
    await state.set_state(Form.travel_date)

@dp.message(Form.travel_date)
async def get_travel_date(message: types.Message, state: FSMContext):
    await state.update_data(travel_date=message.text.strip())
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Normal", callback_data="visa_normal"),
            InlineKeyboardButton(text="Premium", callback_data="visa_premium"),
            InlineKeyboardButton(text="Рандом", callback_data="visa_random"),
        ]
    ])
    await message.answer("Выберите тип визы:", reply_markup=kb)
    await state.set_state(Form.visa_type)

@dp.callback_query(Form.visa_type)
async def visa_type_choice(call: types.CallbackQuery, state: FSMContext):
    val = call.data.replace("visa_", "")
    await state.update_data(visa_type=val)
    await call.message.answer("Введите диапазон дат для выбора (например 1-30):")
    await state.set_state(Form.date_range)
    await call.answer()

@dp.message(Form.date_range)
async def get_date_range(message: types.Message, state: FSMContext):
    await state.update_data(date_range=message.text.strip())
    await message.answer("Введите запрещённые дни (через запятую, например 20,21) или “-” если нет:")
    await state.set_state(Form.forbidden_dates)

@dp.message(Form.forbidden_dates)
async def get_forbidden_dates(message: types.Message, state: FSMContext):
    await state.update_data(forbidden_dates=message.text.strip())
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Первая дата и первое время", callback_data="first_first")],
        [InlineKeyboardButton(text="Первая дата и последнее время", callback_data="first_last")],
        [InlineKeyboardButton(text="Последняя дата и первое время", callback_data="last_first")],
        [InlineKeyboardButton(text="Последняя дата и последнее время", callback_data="last_last")],
        [InlineKeyboardButton(text="Рандомный выбор", callback_data="random")],
    ])
    await message.answer("Выберите стратегию выбора даты и времени:", reply_markup=kb)
    await state.set_state(Form.strategy)

@dp.callback_query(Form.strategy)
async def strategy_choice(call: types.CallbackQuery, state: FSMContext):
    val = call.data
    await state.update_data(strategy=val)
    await call.message.answer("Генерируем архив...")

    data = await state.get_data()
    context = {
        "USER_NAME": data["name"],
        "EMAIL": data["email"],
        "PASSWORD": data["password"],
        "EMAILPASSWORD": data["emailpassword"],
        "TELEGRAM_CHAT_ID": data["chat_id"],
        "TRAVEL_DATE": data["travel_date"],
        "VISA_TYPE": data["visa_type"],
    }

    visa_type = data["visa_type"].lower()
    if visa_type == "normal":
        context["VISA_TYPE_1"] = "Normal"
        context["VISA_TYPE_2"] = "Normal"
    elif visa_type == "premium":
        context["VISA_TYPE_1"] = "Premium"
        context["VISA_TYPE_2"] = "Premium"
    else:
        context["VISA_TYPE_1"] = "Normal"
        context["VISA_TYPE_2"] = "Premium"

    try:
        dr = data["date_range"].replace(" ", "").split("-")
        context["START_DATE"] = int(dr[0])
        context["END_DATE"] = int(dr[1])
    except Exception:
        context["START_DATE"] = 1
        context["END_DATE"] = 31

    forb = data["forbidden_dates"].replace(" ", "")
    if forb == "-" or forb == "":
        context["FORBIDDEN_DATES"] = ""
    else:
        context["FORBIDDEN_DATES"] = ",".join(f"'{d}'" for d in forb.split(",") if d)

    tmpdir = tempfile.mkdtemp()

    # --- Распаковываем static_base.zip ---
    if os.path.exists("static_base.zip"):
        with zipfile.ZipFile("static_base.zip", "r") as basezip:
            basezip.extractall(tmpdir)

    # --- Генерируем шаблоны ---
    for file in os.listdir("templates"):
        if file.endswith(".js"):
            with open(f"templates/{file}", encoding="utf-8") as f:
                template = Template(f.read())
                code = template.render(**context)
            with open(f"{tmpdir}/{file}", "w", encoding="utf-8") as out:
                out.write(code)

    # --- Копируем стратегию ---
    strategy_map = {
        "first_first": "strategy_first_date_first_time.js",
        "first_last": "strategy_first_date_last_time.js",
        "last_first": "strategy_last_date_first_time.js",
        "last_last": "strategy_last_date_last_time.js",
        "random": "strategy_random_date_random_time.js",
    }
    strategy_file = strategy_map.get(data["strategy"])
    if strategy_file:
        with open(f"strategies/{strategy_file}", encoding="utf-8") as f:
            template = Template(f.read())
            code = template.render(**context)
        with open(f"{tmpdir}/strategy.js", "w", encoding="utf-8") as out:
            out.write(code)

    # --- Формируем итоговый архив ---
    zip_path = f"{tmpdir}/scripts.zip"
    with zipfile.ZipFile(zip_path, "w", allowZip64=True) as zipf:
        for f in os.listdir(tmpdir):
            fp = os.path.join(tmpdir, f)
            if os.path.isfile(fp):
                zipf.write(fp, arcname=f)

    with open(zip_path, "rb") as zf:
        await call.message.answer_document(types.BufferedInputFile(zf.read(), "scripts.zip"), caption="Ваш архив готов!")

    await state.clear()
    await call.answer()

if __name__ == "__main__":
    import asyncio
    print("[DEBUG] Бот стартует!")
    asyncio.run(dp.start_polling(bot))
