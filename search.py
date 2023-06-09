from pprint import pprint
import vk_api
from vk_api.exceptions import ApiError

from config import access_token

class Info_users:
    def __init__(self, access_token):    
        self.vkapi = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):

        try:    
            info, = self.vkapi.method('users.get',
            {'user_id': user_id,
            'fields': 'city, sex, bdate, relation'}
            )
        except ApiError as e:
            info ={}
            print(f'error {e}') 
        result = {'name':info['first_name']+' '+info['last_name'] if 'first_name' in info and 'last_name' in info else None,
                'sex':info.get('sex'),
                'city':info.get('city')['title'] if info.get('city') is not None else None,
                'bdate':info.get('bdate')}
        return result
        
    
info = Info_users(access_token)
params = info.get_profile_info(user_id=5808507)

pprint(params)