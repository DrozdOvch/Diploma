import json
import datetime
import requests
from pprint import pprint
import vk_api
from vk_api import VkUpload, upload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from data_base import *
import operator
from operator import itemgetter, attrgetter, methodcaller
offset = 0
from config import token
from config import tokenvk
# vk_authorize = vk_api.VkApi(token=token)
# longpool = VkLongPoll(vk_authorize)





class Vkbot:
    def __init__(self):
        self.authorize = vk_api.VkApi(token=tokenvk)
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk_session)

        self.session = requests.Session()
        self.upload = VkUpload(self.authorize)

    def sender(user_id, text):
        bot.vk_session.method('messages.send',
                             {'user_id': user_id,
                              'message': text,
                              'random_id': 0,
                              })

    def write_message(self, sender, message):
        self.vk_session.method('messages.send', {'user_id': sender,
                                                'message': message,
                                                'random_id': get_random_id()})
    def write_messageattach(self, sender, message, attachment):
        self.vk_session.method('messages.send', {'user_id': sender,
                                                'message': message,
                                                'random_id': get_random_id(),
                                                'attachment': ','.join(attachment)})


    def seeker_name(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': tokenvk,
                  'user_ids': user_id,
                  'v': '5.131'}
        resp = requests.get(url, params)
        response = resp.json()
        information_dict = response['response']
        for i in information_dict:
            for key, value in i.items():
                first_name = i.get('first_name')
                return first_name

    def get_seekers_sex(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': tokenvk, 'user_ids': user_id,
                  'fields': 'sex', 'v': '5.131'}
        resp = requests.get(url, params=params)
        response = resp.json()
        information_list = response['response']
        for i in information_list:
            if i.get('sex') == 2:
                sex_found = 1
                return sex_found
            elif i.get('sex') == 1:
                sex_found = 2
                return sex_found

    def get_city_by_name(self, user_id, city_name):
        url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': tokenvk, 'q': f'{city_name}',
                  'need_all': 0, 'count': 1000, 'v': '5.131'}
        resp = requests.get(url, params=params)
        response = resp.json()
        information_list = response['response']
        list_cities = information_list['items']
        for i in list_cities:
            found_city_name = i.get('title')
            if found_city_name == city_name:
                found_city_id = i.get('id')
                return int(found_city_id)

    def get_city_by_user(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': tokenvk, 'fields': 'city',
                  'user_ids': user_id, 'v': '5.131'}
        resp = requests.get(url, params=params)
        response = resp.json()
        information_cities = response['response']
        for i in information_cities:
            if 'city' in i:
                city = i.get('city')
                id = str(city.get('id'))
                return id
            elif 'city' not in i:
                self.write_message(user_id, 'Введите свой город, пожалуйста!')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        city_name = event.text
                        id_city = self.get_city_by_name(user_id, city_name)
                        if id_city != '' or id_city != None:
                            return str(id_city)

    def age_from(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': tokenvk, 'user_ids': user_id,
                  'fields': 'bdate', 'v': '5.131'}
        resp = requests.get(url, params=params)
        response = resp.json()
        information = response['response']
        for i in information:
            b_date = i.get('bdate')
        date_list = b_date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            actual_year = int(datetime.date.today().year)
            age = actual_year - year
            return age
        elif len(date_list) == 2 or b_date not in information:
            self.write_message(user_id, 'Возраст кандидатов, начиная от ...')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return age

    def age_to(self, user_id):
        self.write_message(user_id, 'Возраст кандидатов до...')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_to = event.text
                return age_to

    def find_candidate(self, user_id):
        url = 'https://api.vk.com/method/users.search'

        age_from = int(self.age_from(user_id))
        age_to = int(self.age_to(user_id))

        print(f'{age_from} up {age_to}')


        params = {'access_token': tokenvk, 'v': '5.131', 'sex': self.get_seekers_sex(user_id),
                  'age_from': age_from, 'age_to': age_to,
                  'city': self.get_city_by_user(user_id), 'relation': '6',
                  'fields': 'is_closed, id, first_name, last_name', 'count': 100}
        res = requests.get(url, params=params)
        resp_json = res.json()
        # print(resp_json)
        resp_dict = resp_json['response']
        resp_list = resp_dict['items']
        for person in resp_list:
            if person.get('is_closed') == False:
                first_name = person.get('first_name')
                last_name = person.get('last_name')
                vk_id = int(person.get('id'))
                vk_link = 'vk.com/id' + str(person.get('id'))
                insert_data_found_users(first_name, last_name, vk_id, vk_link)
            else:
                continue



    def get_photo(self, user_id):
        url = f'https://api.vk.com/method/photos.getProfile'
        params = {'access_token': tokenvk, 'v': '5.131',
                  'type': 'album', 'owner_id': user_id,
                  'album_id': 'profile', 'count': 1000, 'extended': 1,
                  'photo_sizes': 1, 'url': url}

        response = requests.get(url, params=params)
        resp_json = response.json()
        photos = []
        for photo in resp_json['response']['items']:
            photos.append((photo['id'], photo['owner_id'], photo['likes']['count']))
            sorted_photos = sorted(photos, key=operator.itemgetter(2), reverse=True)
            top3_photos = [(id, photo) for id, photo, _ in sorted_photos][:3]
        return top3_photos

    def get_urls(self, user_id):
        url = f'https://api.vk.com/method/photos.getProfile'
        params = {'access_token': tokenvk, 'v': '5.131',
                  'type': 'album', 'owner_id': user_id,
                  'album_id': 'profile', 'count': 1000, 'extended': 1,
                  'photo_sizes': 1, 'url': url}

        response = requests.get(url, params=params)
        resp_json = response.json()
        # pprint(resp_json)
        photos = []
        for photo in resp_json['response']['items']:
            photos.append((photo['id'], photo['sizes'][-1]['url'], photo['likes']['count']))
            sorted_photos = sorted(photos, key=operator.itemgetter(2), reverse=True)
            # print(len(sorted_photos))
            top3 = [(id, photo) for id, photo, _ in sorted_photos][:3]
            top3_urls = [x[1] for x in top3]
        return top3_urls


    # def send_photos(self, user_id):
    #     top3_urls = self.get_urls(self.object_id())
    #     print(top3_urls)
    #     for ul in top3_urls:
    #         r = requests.get(ul)
    #         with open('image.jpg', 'wb') as fd:
    #             for chunk in r.iter_content(4086):
    #                 fd.write(chunk)
    #                 image = 'image.jpg'
    #                 attachment = []
    #                 upload_image = self.upload.photo_messages(photos=image)[0]
    #                 attachment.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
    #                 self.write_messageattach(user_id, '', attachment)


        # link1 = urls[0]
        # link2 = urls[1]
        # link3 = urls[2]
        #
        # image1 = self.session.get(link1, stream=True)
        # image2 = self.session.get(link2, stream=True)
        # image2 = self.session.get(link3, stream=True)
        #
        # photo = self.upload.photo_messages(photos=image1.raw)[0]
        # attachments.append('{}_{}'.format(photo['owner_id'], photo['id']))
        # result = ','.join(attachments)
        # self.write_messageattach(
        #     sender=user_id,
        #     attachment=result,
        #     message='Есть фотографии!')



    def object_id(self):
        tuple_object = select_unseen(offset)
        # print(tuple_object)
        list_object = []
        for i in tuple_object:
            list_object.append(i)
        return(list_object[0])

    def found_object_info(self):
        unseen_info = select_unseen(offset)
        list_object = []
        for i in unseen_info:
            list_object.append(i)
        return f'{list_object[1]} {list_object[2]}, {list_object[3]}'

    def find_object(self, user_id):
        self.write_message(user_id, self.found_object_info())
        self.object_id()
        insert_data_seen_users(self.object_id())
        self.get_photo(self.object_id())
        f_o_photos = self.get_photo(self.object_id())
        # print(f_o_photos)
        if len(f_o_photos) > 1:
            photos_list = []
            for photo in f_o_photos:
                photo_id, owner_id = photo
                photos_list.append(f'{owner_id}_{photo_id}')
                # print(photos_list)
                photos = ','.join(photos_list)
                urls = self.get_urls(self.object_id())
                # photo = ''
                for ul in urls:
                    r = requests.get(ul)
                    with open('image.jpg', 'wb') as fd:
                        for chunk in r.iter_content():
                            fd.write(chunk)
                    photo = 'image.jpg'
                    attachment = []
                    # upload_image = photos_list
                    upload_image = self.upload.photo_messages('image.jpg')[0]
                    attachment.append('photo{}_{}_{}'.format(upload_image['owner_id'], upload_image['id'], upload_image['access_key']))
                    # print(attachment)
            message = 'есть фото!'
            self.write_messageattach(user_id, message, attachment)
            #
            #
            # self.write_message(user_id, attachment)
        elif len(f_o_photos) == 1:
            photo_id, owner_id = f_o_photos[0]
            photos = f'photo{owner_id}_{photo_id}'
            self.write_messageattach(user_id, photos)
        else:

            self.write_message(user_id, 'Фотографий нет')

    # def find_object(self, user_id):
    #     self.write_message(user_id, self.found_object_info())
    #     self.object_id()
    #     insert_data_seen_users(self.object_id())
    #     self.get_photo(self.object_id())
    #     f_o_photos = self.get_photo(self.object_id())
    #     if len(f_o_photos) > 1:
    #         photos_list = []
    #         for photo in f_o_photos:
    #             self.send_photos(user_id)
    #     elif len(f_o_photos) == 1:
    #         photo_id, owner_id = f_o_photos[0]
    #         photos = f'{owner_id}_{photo_id}'
    #         self.write_message(user_id, photos)
    #     else:
    #         self.write_message(user_id, 'Фотографий нет')
    #



bot = Vkbot()

