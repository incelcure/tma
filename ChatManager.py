class ChatManager:
    def __init__(self):
        self.chats = {}  # Словарь для хранения текущих чатов

    def start_chat(self, user1_id, user2_id):
        """Начать новый чат между двумя пользователями"""
        chat_id = (user1_id, user2_id)
        self.chats[chat_id] = []

    def end_chat(self, chat_id):
        """Завершить чат"""
        if chat_id in self.chats:
            del self.chats[chat_id]

    def get_chat_users(self, chat_id):
        """Получить список пользователей в чате"""
        return self.chats.get(chat_id, [])

    def add_message(self, chat_id, message):
        """Добавить сообщение в чат"""
        if chat_id in self.chats:
            self.chats[chat_id].append(message)