import csv
import requests
from bs4 import BeautifulSoup

data_name = []
data_price = []
data_descr = []


# 1_______________________________________________________________________________

for index in range(1, 6):
    for page in range(1, 5):
    
        url = f'https://parsinger.ru/html/index{index}_page_{page}.html'
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



with open('res.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
   
    writer.writerows([[n] + data_descr[index: index + 4] + [p] for n, p, index in zip(data_name, data_price, range(0, 640, 4))])
