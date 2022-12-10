
from bot import *

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseived_message = event.text.lower()
        user_id = str(event.user_id)
        message = event.text.lower()
        sender = (user_id, message.lower())
        list_help = ('Список понятных мне команд: справка, поиск, еще, пока')
        if reseived_message == 'привет!':

            bot.write_message(sender[0], f'Привет! {bot.seeker_name(user_id)}, {list_help}')


        elif reseived_message == 'поиск':
            bot.write_message(sender[0], f'Начнем!')
            create_db()
            bot.find_candidate(user_id)
            bot.find_object(user_id)
            bot.write_message(sender[0], 'Продолжим?')
        elif reseived_message == "еще":
            for i in range(0, 1000):
                offset += 1
                bot.find_object(user_id)
                bot.write_message(sender[0], 'Еще?')
                break
        elif reseived_message == "справка":
            bot.write_message(sender[0], f'{list_help}')


        elif reseived_message == "пока" or reseived_message == "пока!":
            bot.write_message(sender[0], f'До новых встреч, {bot.seeker_name(user_id)}')

        else:
            bot.write_message(sender[0], f'Прости, не понял...{list_help}')

