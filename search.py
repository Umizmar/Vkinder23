from pprint import pprint
import vk_api

from config import access_token

class Info_users:
    def __init__(self, access_token):    
        self.vkapi = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):
            
        info, = self.vkapi.method('users.get',
        {'user_id': user_id,
        'fields': 'city'}
        )
        return info
    
info = Info_users(access_token)
params = info.get_profile_info(user_id=5808507)

pprint(params)