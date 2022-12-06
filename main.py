
from bot import *

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseived_message = event.text.lower()
        user_id = str(event.user_id)
        message = event.text.lower()
        sender = (user_id, message.lower())

        if reseived_message == 'привет!':

            bot.write_message(sender[0], f'Привет! {bot.seeker_name(user_id)}')


        elif reseived_message == 'начнем поиск?':
            bot.write_message(sender[0], f'Начнем!')
            create_db()
            bot.find_candidate(user_id)
            bot.find_object(user_id)
            bot.write_message(sender[0], 'Продолжим?')
        elif reseived_message == "продолжим?":
            for i in range(0, 1000):
                offset += 1
                bot.find_object(user_id)
                break



        elif reseived_message == "пока" or reseived_message == "пока!":
            bot.write_message(sender[0], 'До новых встреч!')

        else:
            bot.write_message(sender[0], 'Прости, не понял...')

