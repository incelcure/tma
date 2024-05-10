import os
from _curses import echo

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Application, ContextTypes, MessageHandler, filters

from ChatManager import ChatManager

load_dotenv()

chat_manager = ChatManager()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Текст сообщения с описанием команд
    message = ("Привет! Я TMA - Анонимный Телеграм Мессенджер.\n\n"
               "Вот список доступных команд и их назначение:\n"
               "/start - Подключиться к анонимному чату\n"
               "/help - Показать справку о боте\n"
               "/stop - Остановить анонимный чат\n")

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def start(update, context):
    # Получаем идентификатор пользователя, который отправил команду /start
    user_id = update.message.from_user.id

    # Получаем список пользователей, участвующих в текущем чате
    chat_users = chat_manager.get_chat_users(user_id)

    # Если пользователь уже участвует в чате, ничего не делаем
    if chat_users:
        await update.message.reply_text("Вы уже находитесь в чате с другим пользователем.")
        return

    # Находим пользователя, с которым нужно начать новый чат
    for chat_id, users in chat_manager.chats.items():
        if user_id in users:
            partner_id = next(uid for uid in users if uid != user_id)
            break
    else:
        await update.message.reply_text("Подождите, пока другой пользователь запустит команду /start.")
        return

    # Создаем новый чат между пользователями
    chat_manager.start_chat(user_id, partner_id)

    # Отправляем уведомление об успешном старте чата
    update.message.reply_text("Вы начали новый анонимный чат. Пришлите свое первое сообщение.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
