import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from search import Info_users
from config import comunity_token, access_token


class BotMessage():
    def __init__(self, comunity_token, access_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_client = Info_users(access_token)
        self.offset = 0
        self.params = {}
        self.worksheets = []
        
    def message_send(self,user_id, message, attachment=None):
        self.vk.method('messages.send',
        {'user_id': user_id,
        'message': message,
        'attachment': attachment,
        'random_id': get_random_id()})

    def request_info(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text
            
    def int_check(self, num):
        try:
            int(num)
        except (TypeError, ValueError):
            return False
        else:
            return True
        
        
        
    def photo (self):
        try:
            self.worksheet = self.worksheets.pop()
            photos = self.vk_client.get_photos(self.worksheet['id'])
            self.photo_string = ''
            for photo in photos:
                self.photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
        except (IndexError):
            self.worksheet = []
        else:
            return
    

    def request_mes(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower()=="привет":
                    self.params = self.vk_client.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Привет, {self.params["name"]}')

                    if self.params['year'] is None:
                        self.message_send(event.user_id, f'Укажите Ваш возраст, пожалуйста')
                        age = (self.request_info())
                        while not self.int_check(age):
                            self.message_send(event.user_id, f'Введите корректный возраст')
                            age = (self.request_info())
                        self.params['year'] = int(age)

                    if self.params['city'] is None:
                        self.message_send(event.user_id, f'Укажите Ваш город, пожалуйста')
                        self.params['city']= self.request_info()

                    if self.params['sex'] == 0:
                        self.message_send(event.user_id, f'Укажите Ваш пол, пожалуйста м/ж')
                        sex = (self.request_info())
                        while sex not in 'мж':
                            self.message_send(event.user_id, f'Введите корректный пол м/ж')
                            sex = (self.request_info())
                        self.params['sex'] = 1 if sex == 'ж' else 2

                    self.message_send(event.user_id, f'Введите "поиск" для поиска')  

                elif event.text.lower()=="поиск":
                    if self.params:

                        self.message_send(event.user_id, f'Идёт поиск...')

                        if self.worksheets:
                            self.photo()   
                        else:
                            self.worksheets = self.vk_client.search_profile(self.params, self.offset)
                            self.photo()
                            self.offset +=10

                        self.message_send(event.user_id, f'Имя:{self.worksheet["name"]} страница:vk.com/id{self.worksheet["id"]}',
                                        attachment=self.photo_string) if self.worksheet\
                                        else self.message_send(event.user_id, f'Не найдено подходящих анкет')
                    else:
                        self.message_send(event.user_id, f'Введите:\n"привет" для инициализации.')

                else:
                    self.message_send(event.user_id, f'Введите:\n"привет" для инициализации.\n"поиск" для поиска')

if __name__=="__main__":
    bot_mes = BotMessage(comunity_token, access_token)
    bot_mes.request_mes()
