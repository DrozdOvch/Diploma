import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from bot import *

#
# def get_token():
#     with open('token.txt', 'r') as f_o:
#         token = f_o.read().strip()
#     return token

keyboard_1 = VkKeyboard(one_time=True)
keyboard_1.add_button('Начнем поиск?', color=VkKeyboardColor.PRIMARY)
keyboard_1.add_button('Пока', color=VkKeyboardColor.NEGATIVE)

keyboard_2 = VkKeyboard(one_time=True)
keyboard_2.add_button('Продолжить!', color=VkKeyboardColor.PRIMARY)
keyboard_2.add_button('Пока!', color=VkKeyboardColor.NEGATIVE)

vk_authorize = vk_api.VkApi(token=get_token())
longpool = VkLongPoll(vk_authorize)


# upload = VkUpload(authorize)


def sender(user_id, text):
    bot.authorize.method('messages.send',
                         {'user_id': user_id,
                          'message': text,
                          'random_id': 0,
                          'keyboard': keyboard})


def write_message_start(sender, message):
    vk_authorize.method('messages.send', {'user_id': sender, 'keyboard': keyboard_1.get_keyboard(),
                                       'message': message, 'random_id': get_random_id()})


def write_message_continue(sender, message):
    vk_authorize.method('messages.send', {'user_id': sender, 'keyboard': keyboard_2.get_keyboard(),
                                       'message': message, 'random_id': get_random_id()})


def write_message_error(sender, message):
    vk_authorize.method('messages.send', {'user_id': sender,
                                       'message': message, 'random_id': get_random_id()})


def write_message_stop(sender, message):
    vk_authorize.method('messages.send', {'user_id': sender,
                                       'message': message, 'random_id': get_random_id()})


for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseived_message = event.text.lower()
        user_id = str(event.user_id)
        message = event.text.lower()
        sender = (user_id, message.lower())

        if reseived_message == 'привет!':

            '''sender - кортеж нужно передавать конкретный индекс'''
            write_message_start(sender[0], 'Привет!')


        elif reseived_message == 'начнем поиск?':
            bot.write_message(user_id, f'Начнем!')
            create_db()
            bot.find_candidate(user_id)
            bot.find_object(user_id, offset)
            write_message_continue(sender[0], 'Продолжим?')
        elif reseived_message == "продолжим?":
            for i in range(0, 1000):
                offset += 1
                bot.find_object(user_id, offset)
                break



        elif reseived_message == "пока" or reseived_message == "пока!":
            write_message_stop(sender[0], 'До новых встреч!')

        else:
            write_message_start(sender[0], 'Прости, не понял...')

keyboard = json.dumps(VkKeyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
