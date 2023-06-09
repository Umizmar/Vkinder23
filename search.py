from datetime import datetime
import vk_api
from vk_api.exceptions import ApiError
from config import access_token
 

class Info_users:
    def __init__(self, access_token):    
        self.vkapi = vk_api.VkApi(token=access_token)

    def bdate_toyear(self,bdate):
        if len(bdate.split('.')) == 3:
            user_year = bdate.split('.')[2] 
            now = datetime.now().year
            return now-int(user_year)
        return None

    def get_profile_info(self, user_id):

        try:    
            info, = self.vkapi.method('users.get',
            {'user_id': user_id,
            'fields': 'city, sex, bdate, relation'}
            )
        except ApiError as e:
            info ={}
            print(f'error {e}') 
        result = {'name':f'{info["first_name"]} {info["last_name"]}' if 'first_name' in info and 'last_name' in info else None,
                'sex':info.get('sex'),
                'city':info.get('city')['title'] if info.get('city') is not None else None,
                'year':self.bdate_toyear(info.get('bdate')) if info.get('bdate') is not None else None
                }
        return result
    
    def search_profile(self, params, offset):
        try:    
            users = self.vkapi.method('users.search',
                                      {'count': 50,
                                       'offset': offset,
                                       'hometown': params['city'],
                                       'sex': 1 if params['sex'] == 2 else 2,
                                       'has_photo': True,
                                       'age_from': params['year'] - 3,
                                       'age_to': params['year'] + 3
                                      }
            
            )
        except ApiError as e:
            users =[]
            print(f'error {e}')
        result = [{'name': f'{item["first_name"]} {item["last_name"]}',
                   'id': item['id']
                   } for item in users['items'] if item['is_closed'] is False
                   ]
        return result
    
    def get_photos(self,id):
        try:    
            photos = self.vkapi.method('photos.get',
            {'owner_id': id,
            'album_id': 'profile',
            'extended':1}
            )
        except ApiError as e:
            photos ={}
            print(f'error {e}')
        
        result = [{'owner_id': item['owner_id'],
                    'id': item['id'],
                    'likes': item['likes']['count'],
                    'comments': item['comments']['count']
                    } for item in photos['items']
                ]
        result.sort(key=lambda x: x['likes']+x['comments'], reverse=True)        
        
        return result[:3]
   