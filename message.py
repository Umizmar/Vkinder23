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

                        self.message_send(event.user_id, f'{self.params["year"]} {self.params["name"]} {self.params["city"]}')
                    if self.params['city'] is None:
                        self.message_send(event.user_id, f'Укажите Ваш город, пожалуйста')
                        self.params['city']= self.request_info()
                        self.message_send(event.user_id, f'{self.params["year"]} {self.params["city"]} {self.params["name"]}')  

                elif event.text.lower()=="поиск":
                    self.message_send(event.user_id, f'Идёт поиск...')

                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photos = self.vk_client.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.worksheets = self.vk_client.search_profile(self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        photos = self.vk_client.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    self.offset +=10

                    self.message_send(event.user_id, f'Имя:{worksheet["name"]} страница:vk.com/id{worksheet["id"]}',
                                      attachment=photo_string)

                else:
                    self.message_send(event.user_id, f'Неизвестная команда')

if __name__=="__main__":
    bot_mes = BotMessage(comunity_token, access_token)
    bot_mes.request_mes()
