import requests
from bs4 import BeautifulSoup
from collections import Counter

url = 'https://parsinger.ru/4.8/3/index.html'

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

data_key = [i.text for i in soup.find('table').find_all('th')]
rowspan = soup.find('td', {'rowspan': "2"})

data_contact = []
data_values = []
for i in soup.find('table').find_all('td'):

    data_emails = []
    if i.find('table'):
        data_emails = [j.text for j in i.find_all('td')]
        data_contact.extend(data_emails)
        data_values.append(dict((data_emails[it], data_emails[it + 1]) for it in range(0, len(data_emails), 2)))

    elif i.text not in data_contact:
        data_values.append(i.text)

from itertools import zip_longest

data_key = data_key * round(len(data_values) / len(data_key))

data = []
d = {}
for i in zip_longest(data_key, data_values, fillvalue=rowspan.text):
    if len(d) < 4:
        d[i[0]] = i[1]
    else:
        d[i[0]] = i[1]
        data.append(d)
        d = {}

print(data)

[{'Имя': 'Иван', 'Фамилия': 'Иванов', 'Возраст': '24', 'Контакты': {'Email': 'ivanov@gmail.com', 'Телефон': '123-45-67'}, 'Хобби': 'Чтение'}, {'Имя': 'Петр', 'Фамилия': 'Петров', 'Возраст': '30', 'Контакты': {'Email': 'petrov@gmail.com', 'Телефон': '987-65-43'}, 'Хобби': 'Чтение'}]

[{'Имя': 'Иван', 'Фамилия': 'Иванов', 'Возраст': '24', 'Контакты': {'Email': 'ivanov@gmail.com', 'Телефон': '123-45-67'}, 'Хобби': 'Чтение'}, {'Имя': 'Петр', 'Фамилия': 'Петров', 'Возраст': '30', 'Контакты': {'Email': 'petrov@gmail.com', 'Телефон': '987-65-43'}, 'Хобби': 'Чтение'}]
