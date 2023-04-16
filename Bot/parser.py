import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
URL_TEMPLATE = "https://www.se.com/ru/ru/download/"
r = requests.get(URL_TEMPLATE)
#print(r.text)
soup = bs(r.text, "lxml")
'''
category = soup.find('span','moreThanFive').find_all('h4')
key_category = []
for i in category:
    key_category.append(i.text)

www_category = []
for i in soup.find('span', 'moreThanFive').find_all('a'):
    www_category.append('https://www.se.com' + i.get('href'))

dict_category = dict(zip(key_category, www_category))

user_get_category = input(key_category)      #dict_category[user_get_category] - для ссылочки
#print(dict_category[user_get_category])
#print(dict_category[user_get_category].replace('?sortByField=Popularity', '?langFilterDisabled=true&keyword=' + input()))
'''

URL = 'https://www.se.com/ru/ru/download/doc-group-type/4493969-Руководства+по+установке+и+эксплуатации./?sortByField=Popularity'
r = requests.get(URL)
soup = bs(r.text, "lxml")
heads = soup.find_all('h5')
links = soup.find_all('li', class_='list-option-doctype')

for i in heads:
    print(i.find('span'))

for i in links:
    print(i.find('a', class_='icons icon-download').get('href'))
    
r = requests.get('https://www.se.com/ru/ru/download/doc-group-type/4493969-Руководства+по+установке+и+эксплуатации./?sortByField=Popularity')
soup = bs(r.text, 'lxml')
heads = soup.find_all('h5')
links = soup.find_all('li', class_='list-option-doctype')
heads_list = []
links_list = []
str_heads_links = str()

for i in heads:
    heads_list.append(i.find('span').text)

for i in links:
    links_list.append(i.find('a', class_='icons icon-download').get('href'))

for i in range(len(heads_list)):
    str_heads_links = str_heads_links + str(i+1) + str(heads_list) + '\n' + str(links_list) + '\n\n'