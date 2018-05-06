#!/usr/bin/python3

import vk
import vk_api
import time
import re

def Involid():
      global inv_id
      write_msg(item['user_id'],"Пришлите удостоверение инвалидности")
      while True:
           response = vk.method('messages.get', values)
           if response['items']:
                    values['last_message_id'] = response['items'][0]['id']
                    write_msg(item['user_id'],"Ваша заявка будет рассмотрена")
                    inv_id = item['user_id']
                    t = Proverka(inv_id)
                    if t == 1:
                        w = open("invalidy.txt","a")
                        w.write(str(item['user_id'])+' ')
                        w.close()
                        #write_msg(item['user_id'],"Ваша заявка принята, чтобы получить помощь напишите !task")
                        break

def Pr_Inv(uid):
    t = open('invalidy.txt','r')
    sps = t.read().split()
    t.close()
    check = str(uid)
    if check in sps:
        return 1

def Pr_Vl(vid):
    t = open('volontery.txt','r')
    sps = t.read().split()
    t.close()
    check = str(vid)
    if check in sps:
        return 1

def Opoveshenie(ll):
    y = open("vol_mest.txt",'r')
    vol = y.read().split('%%%')
    y.close()
    print(vol)
    we = [] 
    for i in range(len(vol)):
             if ll in vol[i]: 
                  we += [vol[i]]       
    f = re.compile('[АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]')
    print(we)
    for i in range(len(we)):
        we[i] = f.sub('',we[i])
    t = []
    for i in range(len(we)):
        t += re.findall('https://vk.com/id[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]',we[i])
    y = re.compile('[https:/vk.comid]')
    for i in range(len(t)):
         t[i] = y.sub('',t[i])
    print(t)
    return t
#while True:
           #response = vk.method('messages.get', values)
           #if response['items']:
                    #values['last_message_id'] = response['items'][0]['id']
                    #for i in range(len(t)):
                    #         write_msg(t[i],'В вашем районе нужна помощь инвалиду!')
                    #return None
#q = Opoveshenie('Юго-Западная')
#print(q)

def Proverka(inv):
      write_msg(297399806,'Вам поступила заявка, проверьте сообщество')  
      while True:
           response = vk.method('messages.get', values)
           if response['items']:
                    values['last_message_id'] = response['items'][0]['id']
                    if response['items'][0]['body'] == "Одобрено":
                        write_msg(inv,"Оповещаем об успешности одобрения документа.Кодовое сообщение на получение помощи - !task.\nНапишите его, если Вы нуждаетесь в помощи")
                        return 1

def Pomosh():
     write_msg(item['user_id'], 'Напишите Ваше местоположение\nПример:Покрышкино')
     while True:
           response = vk.method('messages.get', values)
           if response['items']:
                    values['last_message_id'] = response['items'][0]['id']
                    o = open('task.txt','a')
                    task = o.write(str(response['items'][0]['body'])+'%%%')
                    tt = response['items'][0]['body']
                    o.close() 
                    ch = Zadanie(tt)
                    cc = Opoveshenie(tt)
                    for i in range(len(cc)):
                        write_msg(int(cc[i]),'Инвалид в указанном Вами районе нуждается в помощи.')
                    if ch == 1:
                        pass
                    elif ch == 0:
                        write_msg(item['user_id'],"К сожалению, в этом районе пока нет волонтеров\nВы можете связаться с нами по телефону - 89853556755 и мы попробуем решить Вашу проблему")
                    break


def Zadanie(ll):
    y = open('vol_mest.txt','r')
    t = y.read().split('%%%')
    y.close() 
    print(t[1])
    y = 0
    for i in range(len(t)-1):
        if ll in t[i]:
            write_msg(item['user_id'],'Вам может помочь:\n'+t[i])  
            y+=1
    if y>0:
        return 1
    else:
        return 0
 
def Volonter():
      global volontery
      write_msg(item['user_id'],"Напишите пожалуйста свои данные\n1.Улица, где Вы чаще всего находитесь\n2.Имя\n3.Мобильный телефон\n4.Аккаунт в Telegram\nПример:\n Покрышкино\nАлексей\n89853556755\nтелеграм - @noprazd")
      while True:
           response = vk.method('messages.get', values)
           if response['items']:
                    values['last_message_id'] = response['items'][0]['id']
                    t = open('volontery.txt','a')
                    t.write(str(item['user_id'])+' ')
                    t.close()
                    t = open('vol_mest.txt','a')
                    t.write("ВК: https://vk.com/id"+str(item['user_id'])+'\n'+str(response['items'][0]['body']+'%%%'))
                    t.close()
                    write_msg(item['user_id'],'Спасибо за то, что делаете мир лучше!\nНадеюсь Вы понимаете, насколько важна Ваша помощь и надеемся, на Вашу ответственность в этом деле')
                    break

vk = vk_api.VkApi(token='77777dfb2b3caa9942cf9a2da42e168f33d2c925206f40bc7586584ab743454f152952eee5c56546b9321')
values = {'out':0,'count':100,'time_offset':60}
def write_msg(user_id, s):
    vk.method('messages.send',{'user_id':user_id,'message':s})

while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
        for item in response['items']: 
             # if и elif не забыть убрать потом!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
             if response['items'][0]['body'] == '!task': 
                 Pomosh() 
             elif Pr_Inv(item['user_id']) == 1:
                 write_msg(item['user_id'],"Вы уже есть в списке!Напишите о помощи(!task)")
             elif Pr_Vl(item['user_id']) == 1:
                 write_msg(item['user_id'],"Вы являетесь волонтером.\nБудьте на чеку, так как скоро может понадобиться Ваша помощь")
             elif response['items'][0]['body'] == '1':
                Involid()
                continue
             elif response['items'][0]['body'] == '2':
                Volonter() 
                continue 
             else:
                write_msg(item['user_id'],'Напишите 1(Инвалид) или 2(Волонтер)')
        time.sleep(1)
