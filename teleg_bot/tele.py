#!/home/prazd/anaconda3/bin/python3.6
import telebot
import json
token = '490652935:AAGwy8QE1tR7J53ZP3jN2nR6ELD1jXsradM'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["task"])
def task(message):
    bot.send_message(message.chat.id,'ЗАДАНИЕ')

@bot.message_handler(commands=["start"])
def mes(message):
    with open('inv.txt','r') as infile:
         i = infile.read().split('\n')
    with open('vol.txt','r') as volfile:
         v = volfile.read().split('\n')
    if str(message.chat.id) in i:
         bot.send_message(message.chat.id,'Вы зарегистрированы как инвалид, отправьте /task для получения помощи')

    elif str(message.chat.id) in v:
        bot.send_message(message.chat.id,'Вы зарегистрироаваны, как волонтер')
         #if str(message.chat.id) in e:
         #bot.send_message(message.chat.id,'Вы уже есть в списке')
    else:
         markup = telebot.types.ReplyKeyboardMarkup()
         markup.row('Хочу выступать, как волонтер','Хочу зарегаться, как инвалид')
         send = bot.send_message(message.chat.id,'Здравствуйте!\nВыберите один из предложенных вариантов',reply_markup=markup)
         bot.register_next_step_handler(send,variant)

def variant(message):
    w = ['Хочу выступать, как волонтер']
    if message.text != w[0]:
        mark = telebot.types.ReplyKeyboardMarkup()
        mark.row('К сожалению его нет')
        ud_in = bot.send_message(message.chat.id,'Пришлите удостоверение инвалида',reply_markup=mark)
        bot.register_next_step_handler(ud_in,reg_inv)
    else:
        ud_vo = bot.send_message(message.chat.id,'''Напишите свои контактные данные в формате: \n1.Место, где Вы чаще всего бываете\n2.Имя\n3.Номер телефона'''
        '''\nПример:\nОдиново\nАлексей\n89853556755''')
        bot.register_next_step_handler(ud_vo,reg_vo)

def reg_inv(message):
    if message.text == 'К сожалению его нет':
        bot.send_message(message.chat.id,'''Нам очень жаль, но оно необходимо для продолжения
        регистрации\nЕсли у Вас возникнли вопросы, то Вы можете позвонить по телефону - 89853556755 или написать свой вопрос в телеграм - ...''')
    with open('id.txt','a') as id:
        id.write(str(message.chat.id))
    m = bot.send_message(316152758,'Чувак хочет инвалидом зарегаться')
    bot.register_next_step_handler(m,resh)

def resh(message):
    if message.text == "OK":
        with open('id.txt','r') as dob_inv:
            t = dob_inv.read().split('\n')
        print(t)
        with open('inv.txt','a') as d_i:
            w = d_i.write(t[-1])
        print(t[-1])
        bot.send_message(int(t[-1]),'Все в порядке')

def reg_vo(message):
    a = message.text.split('\n')
    print(a)
    bot.send_message(message.chat.id,'ага')

if __name__ == '__main__':
    bot.polling(none_stop=True)
