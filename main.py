import logging
import asyncio
import sys
from dotenv import load_dotenv
import os
import re
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.filters import Command
logging.basicConfig(level=logging.INFO)

load_dotenv()
print(re.__doc__)

#if sys.platform == "win32":
#   loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

# 🔹 Настройка логирования

# 🔹 Токен бота и ID админа
TOKEN = os.getenv("TOKEN")  # <-- Вставь свой токен бота  
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
GROUP_ID = int(os.getenv("GROUP_ID", 0))  # ID администратора




# 🔹 Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# 📌 Команда /start
@router.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Перейти на сайт", url="https://www.keyturkiye.com/")],
        [InlineKeyboardButton(text="🔥 Консультация", url="https://t.me/KeyturSupport_bot")],
        [InlineKeyboardButton(text="🔥 Подать заявку в группу", callback_data="request_access")]
    ])
    await message.answer(f"👋 Привет, {message.from_user.first_name}! Выберите нужную опцию:", reply_markup=keyboard)

# 📌 Обработка заявки на вступление
@router.callback_query(lambda c: c.data == "request_access")
async def process_request(callback_query: CallbackQuery):
    user = callback_query.from_user
    await bot.send_message(
        ADMIN_ID,
        f"⚡ Пользователь {user.full_name} (@{user.username}) хочет вступить в группу.\n"
        f"Разрешить? /approve_{user.id}"
    )
    await callback_query.answer("✅ Ваша заявка отправлена администратору.")

# ✅ Админ подтверждает заявку
@router.message(lambda message: message.text.startswith("/approve_"))
async def approve_user(message: Message):
    try:
        user_id = int(message.text.split("_")[1])
        invite_link = "https://t.me/+4IcY80QaPMozNjVi"  # Укажи реальную ссылку на группу
        await bot.send_message(user_id, f"✅ Ваша заявка одобрена! Вот ссылка: [Вступить]({invite_link})", parse_mode="Markdown")
        await bot.send_message(GROUP_ID, f"🎉 Пользователь [{user_id}](tg://user?id={user_id}) присоединился!")
    except Exception as e:
        logging.error(f"Ошибка: {e}")

# 🚀 Запуск бота
async def main():
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске: {e}")

if __name__ == "__main__":
    logging.info("🤖 Бот запущен!")
    asyncio.run(main())
