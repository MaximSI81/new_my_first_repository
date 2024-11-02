import json
import requests
from bs4 import BeautifulSoup

data_name = []
data_price = []
data_descr = []
data = []
for index in range(1, 6):
    for page in range(1, 5):
        url = f'https://parsinger.ru/html/index{index}_page_{page}.html'
        session = requests.Session()
        response = session.get(url=url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')

        name = soup.find_all('a', class_="name_item")
        data_name += [n.text.strip() for n in name]
        price = soup.find_all('p', class_='price')
        data_price += [p.text for p in price]
        data_descr += [list(map(lambda x: x.text.split(': '), i.find_all('li'))) for i in
                       soup.find_all('div', class_='description')]

for n, d, p in zip(data_name, data_descr, data_price):
    data.append({
        "Наименование": n,
        d[0][0].strip(): d[0][1].strip(),
        d[1][0].strip(): d[1][1].strip(),
        d[2][0].strip(): d[2][1].strip(),
        d[3][0].strip(): d[3][1].strip(),
        "Цена": p
    })

with open('res.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
