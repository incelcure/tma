import os
from _curses import echo

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Application, ContextTypes, MessageHandler, filters

load_dotenv()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Текст сообщения с описанием команд
    message = ("Привет! Я TMA - Анонимный Телеграм Мессенджер.\n\n"
               "Вот список доступных команд и их назначение:\n"
               "/start - Показать список команд\n"
               "/help - Показать справку о боте\n"
               "/connect - Подключиться к анонимному чату\n"
               "/stop - Остановить анонимный чат\n")

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("help", help))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
