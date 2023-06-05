import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token


class BotMessage():
    def __init__(self,comunity_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        
    def message_send(self,user_id, message, attachment=None):
        self.vk.method('messages.send',
        {'user_id': user_id,
        'message': message,
        'attachment': attachment,
        'random_id': get_random_id()})

    def request_mes(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower()=="привет":
                    self.message_send(event.user_id, f'Привет, {event.user_id}')
                elif event.text.lower()=="поиск":
                    self.message_send(event.user_id, f'Идёт поиск...')
                elif event.text.lower()=="пока":
                    self.message_send(event.user_id, f'До свидания, {event.user_id}')
                else:
                    self.message_send(event.user_id, f'Неизвестная команда')

if __name__=="__main__":
    bot_mes = BotMessage(comunity_token)
    bot_mes.request_mes()
