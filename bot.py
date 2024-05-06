import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    # Текст сообщения с описанием команд
    message = ("Привет! Я твой телеграм-бот.\n\n"
               "Вот список доступных команд и их назначение:\n"
               "/start - Показать список команд\n"
               "/help - Показать справку о боте\n"
               "/connect - Подключиться к анонимному чату\n"
               "/stop - Остановить анонимный чат\n")

    # Отправка сообщения с описанием команд
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def main():
    # Ваш токен доступа
    token = os.getenv('TG_BOT_TOKEN')

    # Инициализация бота
    updater = Updater(token, use_context=True)

    # Получение диспетчера для регистрации обработчиков команд
    dispatcher = updater.dispatcher

    # Добавьте обработчики команд здесь
    dispatcher.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
