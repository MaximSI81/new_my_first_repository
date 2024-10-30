import csv
import requests
from bs4 import BeautifulSoup

data_name = []
data_price = []
data_descr = []

for i in range(1, 5):
    # 1_______________________________________________________________________________

    url = f'https://parsinger.ru/html/index4_page_{i}.html'
    session = requests.Session()
    response = session.get(url=url)
    response.encoding = 'utf-8'

    # 2_______________________________________________________________________________

    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find_all('a', class_="name_item")
    data_name += [n.text.strip() for n in name]
    price = soup.find_all('p', class_='price')
    data_price += [p.text for p in price]
    description = soup.find_all('div', class_='description')
    for j in description:
        data_descr += [i.text.split(':')[1].strip() for i in j.find_all('li')]

# 3_______________________________________________________________________________
columns = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объем буферной памяти', 'Цена']

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(columns)
    writer.writerows([[n] + data_descr[index: index + 4] + [p] for n, p, index in zip(data_name, data_price, range(0, 128, 4))])
