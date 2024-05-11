import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
# from aiogram.utils import executor
from ChatManager import ChatManager

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)
chat_manager = ChatManager()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id

    chat_users = chat_manager.get_chat_users(user_id)

    if chat_users:
        await message.answer("Вы уже находитесь в чате с другим пользователем.")
        return

    for chat_id, users in chat_manager.chats.items():
        if user_id in users:
            partner_id = next(uid for uid in users if uid != user_id)
            break
    else:
        await message.answer("Подождите, пока другой пользователь запустит команду /start.")
        return

    chat_manager.start_chat(user_id, partner_id)

    await message.answer("Вы начали новый анонимный чат. Пришлите свое первое сообщение.")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    message_text = ("Привет! Я TMA - Анонимный Телеграм Мессенджер.\n\n"
                    "Вот список доступных команд и их назначение:\n"
                    "/start - Подключиться к анонимному чату\n"
                    "/help - Показать справку о боте\n"
                    "/stop - Остановить анонимный чат\n")
    await message.answer(message_text)


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    user_id = message.from_user.id
    chat_manager.end_chat(user_id)
    await message.answer("Чат завершен.")


@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    chat_users = chat_manager.get_chat_users(user_id)

    if not chat_users:
        return

    for chat_id, users in chat_manager.chats.items():
        if user_id in users:
            partner_id = next(uid for uid in users if uid != user_id)
            break
    else:
        return

    await bot.send_message(partner_id, text)
    await chat_manager.add_message((user_id, partner_id), text)


async def main():
    # Запускаем обработку входящих сообщений
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
    # dp.start_polling()
