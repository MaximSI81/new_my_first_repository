import json
import requests
from bs4 import BeautifulSoup

data_name = []
data_price = []
data_descr = []
data = []
for page in range(1, 5):

    url = f'https://parsinger.ru/html/index4_page_{page}.html'
    session = requests.Session()
    response = session.get(url=url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find_all('a', class_="name_item")
    data_name += [n.text.strip() for n in name]
    price = soup.find_all('p', class_='price')
    data_price += [p.text for p in price]
    description = soup.find_all('div', class_='description')
    for j in description:
        data_descr += [i.text.split(':')[1].strip() for i in j.find_all('li')]

for n, p, index in zip(data_name, data_price, range(0, 128, 4)):
    data.append({
        "Наименование": n,
        "Бренд": data_descr[index:index + 4][0],
        "Форм-фактор": data_descr[index:index + 4][1],
        "Ёмкость": data_descr[index:index + 4][2],
        "Объем буферной памяти": data_descr[index:index + 4][3],
        "Цена": p
    })

with open('res.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
