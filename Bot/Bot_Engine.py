import telebot
import requests
import pandas as pd

from bs4 import BeautifulSoup as bs
from telebot import types

#Таблица
file = "..\DB.xlsx"
DB = pd.ExcelFile(file)
ASUTP = DB.parse('ASUTP')

#5885003771:AAEUhLIfbXa7HU_Wnb8Kc5oZRnyUdNcC5mU
bot = telebot.TeleBot("5885003771:AAEUhLIfbXa7HU_Wnb8Kc5oZRnyUdNcC5mU", parse_mode=None)

#Создаем список комманд на поломки
Command_List_Of_Crashes = []
for i in range(len(ASUTP)):
    if str(ASUTP["Объект подлежащий ремонту"].iloc[i]).split()[0] != 'nan':
        Command_List_Of_Crashes.append(str(ASUTP["Объект подлежащий ремонту"].iloc[i]).split()[0])

Command_List_Of_Details = []
for i in range(len(ASUTP)):
    Command_List_Of_Details.append(str(ASUTP["Возможные отказы технических средств АСУ ТП"].iloc[i]).split()[0])

@bot.message_handler(commands = ['start'])
def Pass(message):
    bot.send_message(message.chat.id, 'Здравствуйте, этот бот создан специально в качестве решения кейса от компании Транснефть \n /crash - выдача списка поломок \n /info - выдача списка категорий')

#Отзыв на /crash
@bot.message_handler(commands=['crash'])
def Data_crash(message):
    Data = str()
    for i in range(len(ASUTP)):
        if str(ASUTP["Объект подлежащий ремонту"].iloc[i]) != 'nan':
            Data =  Data + "/" + str(ASUTP["Объект подлежащий ремонту"].iloc[i]) + "\n"
    bot.send_message(message.chat.id, "Выберите объект подлежащий ремонту:\n \n" + Data)

#тута выводится список возможных отказов и подготовка к ремонту
@bot.message_handler(commands = Command_List_Of_Crashes)
def Crashes(message):
    
    Data_Otkaz = str()
    
    for i in range(len(ASUTP['Объект подлежащий ремонту'])):
        if message.text == "/" + str(ASUTP['Объект подлежащий ремонту'].iloc[i]).split()[0]:
            Podgotovka_k_Remontu = str(ASUTP['Подготовка к ремонту'].iloc[i])
            index_of_object = i   #ПОФИКСИТЬ НАДА!!!!!!!!!!!
                                    #ПОФИКСИТЬ НАДА!!!!!!!!!!!
                                    #ПОФИКСИТЬ НАДА!!!!!!!!!!!
    while (("/" + str(ASUTP['Объект подлежащий ремонту'].iloc[index_of_object]).split()[0] == message.text) or (str(ASUTP['Объект подлежащий ремонту'].iloc[index_of_object]).split()[0] == 'nan')) and (index_of_object != (len(ASUTP['Возможные отказы технических средств АСУ ТП'])-1)):
        print("1")
        Data_Otkaz = Data_Otkaz + "/" + str(ASUTP['Возможные отказы технических средств АСУ ТП'].iloc[index_of_object]) + "\n"
        index_of_object = index_of_object + 1
    bot.send_message(message.chat.id, "Что требуется подготовить для ремонта:\n \n" + Podgotovka_k_Remontu)
    bot.send_message(message.chat.id, "Возможные отказы:\n \n" + Data_Otkaz) 

#тута выводятся два последних сообщения
@bot.message_handler(commands = Command_List_Of_Details)
def Details(message):
    for i in range(len(ASUTP['Возможные отказы технических средств АСУ ТП'])):
        if message.text == "/" + str(ASUTP['Возможные отказы технических средств АСУ ТП'].iloc[i]).split()[0]:
            row = i
            
    bot.send_message(message.chat.id, "Вероятные причины:\n \n" + ASUTP['Вероятные причины'].iloc[row])   
    bot.send_message(message.chat.id, "Способы предупреждения и ликвидации последующих аварийных ситуаций:\n \n" + ASUTP['Способы предупреждения и ликвидации последующих аварийных ситуаций'].iloc[row])     
 
#===============================================#
#                                               #
#                                               #
#                парсинг                        #
#                                               #
#                                               #
#===============================================#

URL_TEMPLATE = "https://www.se.com/ru/ru/download/"
r = requests.get(URL_TEMPLATE)
soup = bs(r.text, "lxml")
Global_key_category = ''

category = soup.find('span','moreThanFive').find_all('h4')
key_category = []
for i in category:
    key_category.append(i.text)

www_category = []
for i in soup.find('span', 'moreThanFive').find_all('a'):
    www_category.append('https://www.se.com' + i.get('href'))

dict_category = dict(zip(key_category, www_category))
dict_category_links = dict_category
list_category_links = []
for i in range(len(key_category)):
    dict_category_links[key_category[i]] = str(dict_category[key_category[i]].replace("?sortByField=Popularity","?langFilterDisabled=true&keyword="))

@bot.message_handler(commands=['info'])
def Shneider_parsing_info(message):
    str_list_key_category = str()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    
    for i in range(len(key_category)):
        str_list_key_category = str_list_key_category + str(i+1) + '. ' + str(key_category[i] + '\n')
        markup.add(types.KeyboardButton(key_category[i]))
     
    bot.send_message(message.chat.id, "Выберите категорию:\n\n" + str_list_key_category, reply_markup=markup)

choosed_category = str()
#@bot.message_handler(func=lambda message: message.text == "жопа")
@bot.message_handler(func=lambda message: True)
def handle_message(message):
     #костыль
    global choosed_category
    for i in range(len(key_category)):
        print(message.text)
        if message.text == key_category[i]:
            
            r = requests.get(dict_category[key_category[i]])
            soup = bs(r.text, 'lxml')
            heads = soup.find_all('h5')
            links = soup.find_all('li', class_='list-option-doctype')
            heads_list = []
            links_list = []
            #str_heads_links = str()
            choosed_category = key_category[i]
            #Global_key_category = key_category[i]
            bot.send_message(message.chat.id, 'Ссылка на ресурс по поиску:\n\n' + dict_category[key_category[i]]) #вывод ссылки
            bot.send_message(message.chat.id, 'Отправьте ключевое слово, название продукта или номер файла:')
    schet = 0

    for i in range(len(key_category)):
        if message.text == key_category[i]:
            schet = schet + 1
        print(schet)
    
    if schet == 0:
        r = requests.get(str(dict_category_links[choosed_category])+str(message.text))
        print(r)
        soup = bs(r.text, 'lxml')
        heads = soup.find_all('h5')
        links = soup.find_all('li', class_='list-option-doctype')
        heads_list = []
        links_list = []
        #tr_heads_links = str()
        for i in heads:
            heads_list.append(i.find('span').text)
            print("heads")
        for i in links:
            links_list.append(i.find('a', class_='icons icon-download').get('href'))
            print("links")
        print(heads_list)
        if len(heads_list) > 0:
            for i in range(len(heads_list)):  
                bot.send_message(message.chat.id, str(i+1) + '. ' + str(heads_list[i]) + '\n' + str(links_list[i]).replace("//", ""))
        else:
            bot.send_message(message.chat.id, "Ничего не найдено")

def handle_regex(message):
    global choosed_category
    schet = 0
    j = 0
    for j in range(len(key_category[j])):
        if (message.text == key_category[j]) or (message.text == '/start'):
            schet = schet +1
        print(schet)
    if schet == 0:
        print(schet)
        r = requests.get(dict_category[key_category[choosed_category]].replace("?sortByField=Popularity","?langFilterDisabled=true&keyword="+message.text))
        soup = bs(r.text, 'lxml')
        heads = soup.find_all('h5')
        links = soup.find_all('li', class_='list-option-doctype')
        heads_list = []
        links_list = []
        #tr_heads_links = str()
        for i in heads:
            heads_list.append(i.find('span').text)
            print("heads")
        for i in links:
            links_list.append(i.find('a', class_='icons icon-download').get('href'))
            print("links")
        for i in range(len(heads_list)):  
            bot.send_message(message.chat.id, str(i+1) + '. ' + str(heads_list[i]) + '\n' + str(links_list[i]).replace("//", ""))

    

bot.infinity_polling()
