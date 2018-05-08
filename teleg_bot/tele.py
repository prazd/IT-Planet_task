#Нужна бд mysql, где есть 2 databases - inv и vol
#в inv 1 таблица id(id INT)
#в vol таблица info(id INT, name TEXT, place TEXT, mob TEXT, teleg TEXT)
#Также нужен файл id.txt

import telebot
import MySQLdb
import subprocess

token = 'токен'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["task"])
def task(message):
    conn = MySQLdb.connect('БД vol')
    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('select id from info')
    chch = cursor.fetchall()
    chspis = []
    for i in chch:
        for g in i:
            chspis+=[g]
    if message.chat.id in chspis:
        bot.send_message(message.chat.id,'Вы волонтер и не можете пользоваться /task')
    else:
        cursor.execute('select place from info')
        che = cursor.fetchall()
        cche = []
        for i in che:
           for z in i:
               cche+=[z]
        t = set(cche)
        m = list(t)
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in m:
            keyboard.add(telebot.types.InlineKeyboardButton(text="{}".format(i),callback_data="{}".format(i)))
        no_place = telebot.types.InlineKeyboardButton(text="Места нет в списке",callback_data='none')
        keyboard.add(no_place)
        bot.send_message(message.chat.id,'Это места, где есть зарегестрированные волонтеры',reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def gorod(call):
    if call.data == "none":
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Обратитесь за помощью - @noprazd')
    else:
        conn = MySQLdb.connect('БД vol')
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        cursor.execute('select name, mob, teleg from  info where place =\'{}\''.format(call.data))
        otv = cursor.fetchall()
        cursor.execute('select id from info where place =\'{}\''.format(call.data))
        rassyl = cursor.fetchall()
        print('rassyl_id = '+str(rassyl))
        spis = []
        print(otv)
        for i in otv:
            spis+=[i]
        print(spis)
        col = len(spis)
        q = ""
        sc = 0
        for i in range(col):
            e = i
            for z in spis[i]:
                 q +=str(z)+'\n'
                 sc+=1
                 if sc == 3:
                     q+='\n'
                     sc = 0
        print(q)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Вот, кто Вам может помочь:\n'+q)
        for i in range(len(rassyl)):
            bot.send_message(rassyl[i][0],'Инвалид в Вашем районе нуждается в помощи')

@bot.message_handler(commands=["start"])
def mes(message):
    def mysql_check():
        connect = MySQLdb.connect('БД inv')
        cursor = connect.cursor()
        cursor.execute('select * from id')
        check_inv = cursor.fetchall()
        for i in check_inv:
            for z in i:
              print(z)
              if z == message.chat.id:
                    connect.close()
                    return 1
        conn = MySQLdb.connect('БД vol')
        cur = conn.cursor()
        cur.execute('select id from info')
        check_vol = cur.fetchall()
        for q in check_vol:
            for y in q:
                if y == message.chat.id:
                    conn.close()
                    return 2
        connect.close()
        conn.close()
    c = mysql_check()
    print(c)
    if c == 1:
        bot.send_message(message.chat.id,'Вы уже зарегестрированы как инвалид, отправьте /task для получения помощи')
    elif c == 2:
        bot.send_message(message.chat.id,'Вы зарегистрированы как волонтер, ждите пока к Вам не обратятся за помощью')

    else:
         markup = telebot.types.ReplyKeyboardMarkup()
         markup.row('Хочу зарегистрироваться как волонтер','Хочу зарегистрироваться как инвалид')
         send = bot.send_message(message.chat.id,'Здравствуйте!\nВыберите один из предложенных вариантов',reply_markup=markup)
         bot.register_next_step_handler(send,variant)

def variant(message):
    w = ['Хочу зарегистрироваться как волонтер']
    if message.text != w[0]:
        mark = telebot.types.ReplyKeyboardMarkup()
        mark.row('/task')
        connect = MySQLdb.connect('БД inv')
        cursor = connect.cursor()
        cursor.execute("insert into id values("+str(message.chat.id)+")")
        connect.commit()
        connect.close()
        bot.send_message(message.chat.id,'Мы внесли Вас в базу, Вы уже можете получить помощь',reply_markup=mark)

    else:
        ud_vo = bot.send_message(message.chat.id,'''Напишите свои контактные данные в формате: \n1.Место, где Вы чаще всего бываете\n2.Имя\n3.Номер телефона'''
        '''\nПример:\nОдиново\nАлексей\n89853556755''')
        bot.register_next_step_handler(ud_vo,reg_vo)

def resh(message):
    if message.text == "OK":
        with open('id.txt','r') as dob_inv:
            t = dob_inv.read().split('\n')
        print(t)
        subprocess.call('echo "" > id.txt',shell=True)
        connect = MySQLdb.connect('БД inv')
        cursor = connect.cursor()
        cursor.execute("insert into id values("+t[-1]+")")
        connect.commit()
        connect.close()
        bot.send_message(int(t[-1]),'Вы зарегестрированы, как инвалид. Чтобы начать работу нажмите /task')

def reg_vo(message):
    a = message.text.split('\n')
    e=[]
    e+=a
    e+=[message.from_user.username]
    print(e)
    connect = MySQLdb.connect('БД vol')
    connect.set_character_set('utf8')
    cursor = connect.cursor()
    try:
        cursor.execute('insert into info(id, place, name, mob, teleg) values({},\'{}\',\'{}\',\'{}\',\'@{}\')'.format(str(message.chat.id),e[0],e[1],e[2],'@'+e[3]))
        connect.commit()
        connect.close()
        bot.send_message(message.chat.id,'Вы делаете мир лучше!')
    except IndexError:
        bot.send_message(message.chat.id,'Данные указаны в неправильном формате!')



@bot.message_handler(content_types='[text]')
def otvet(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    w = telebot.types.InlineKeyboardButton(text='Можете также попробовать нашего бота вк',url = 'https://vk.com/club163425064')
    keyboard.add(w)
    bot.send_message(message.chat.id,'Чтобы начать работу с ботом отправьте /start',reply_markup=keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)
