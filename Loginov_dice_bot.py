import random
import telebot
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('ТОКЕН')
last_time = datetime.now()
last_stats_list = []


def dice_throw(number, message):
    global last_time
    roll = random.randint(1, number)
    dice = random.randint(1, 4)
    photo = open(f'D20/{roll}/{roll}_{dice}.jpeg', 'rb')
    bot.send_photo(message, photo)
    last_time = datetime.now()


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Рады приветствовать тебя,'
                     f' <b><em>{message.from_user.first_name}'
                     f'{message.from_user.last_name}!'
                     f'</em></b>', parse_mode='HTML')
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("⚔️🛡Roll 20🛡⚔️")
    btn2 = types.KeyboardButton("⚔️🛡Roll 12🛡⚔️")
    btn3 = types.KeyboardButton("⚔️🛡Roll 10🛡⚔️")
    btn4 = types.KeyboardButton("⚔️🛡Roll 6🛡⚔️")
    btn5 = types.KeyboardButton("⚔️🛡Roll 4🛡⚔️")
    btn6 = types.KeyboardButton("Генерация статов персонажа")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, text='Какой '
                     'DICE решит твою судьбу?'.format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global last_time
    global last_stats_list
    delta = datetime.now() - last_time
    if delta.seconds > 0.5:
        if (message.text == "⚔️🛡Roll 20🛡⚔️"):
            dice_throw(number=20, message=message.chat.id)
        elif (message.text == "⚔️🛡Roll 12🛡⚔️"):
            dice_throw(number=12, message=message.chat.id)
        elif (message.text == "⚔️🛡Roll 10🛡⚔️"):
            dice_throw(number=10, message=message.chat.id)
        elif (message.text == "⚔️🛡Roll 6🛡⚔️"):
            dice_throw(number=6, message=message.chat.id)
        elif (message.text == "⚔️🛡Roll 4🛡⚔️"):
            dice_throw(number=4, message=message.chat.id)
        elif (message.text == "Генерация статов персонажа"):
            i = 0
            stats_list = ''
            for i in range(6):
                d6 = [random.randint(1, 6), random.randint(1, 6),
                      random.randint(1, 6), random.randint(1, 6)]
                d6.sort()
                stats = d6[1] + d6[2] + d6[3]
                stats_list += f' {stats},'
                last_stats_list.append(stats)
                i += 1
            bot.send_message(message.chat.id,
                             text=f'{stats_list} вот ваши цифры.')
            bot.send_message(message.chat.id, text='<b>Распределите их'
                             'согласно выбранному классу.</b>',
                             parse_mode='HTML')
            last_time = datetime.now()
    else:
        bot.send_message(message.chat.id, text='Терпение, путник, рука судьбы'
                         ' должна размяться перед новым броском!')


bot.polling(none_stop=True)
