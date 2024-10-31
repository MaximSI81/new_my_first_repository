import csv
import requests
from bs4 import BeautifulSoup

def func(sp):
    data = []
    for i in sp:
        data.append([li.text.split(':')[1].strip() for li in i.find_all('li')])
    return data
        



data_lincs = []
data_name = []
data_price = []
data_descr = []
data_article = []
data_old_price = []
data_stock = []


for i in range(1, 5):
    # 1_______________________________________________________________________________

    url = f'https://parsinger.ru/html/index1_page_{i}.html'
    session = requests.Session()
    response = session.get(url=url)
    response.encoding = 'utf-8'

    # 2_______________________________________________________________________________
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    data_lincs += [i.find('a')['href'] for i in soup.find_all(class_='img_box')]


    for linc in range(1, 33):
            
        # 1.1 _______________________________________________________________________
        resp = requests.get(f'https://parsinger.ru/html/watch/1/1_{linc}.html')
        resp.encoding = 'utf-8'
    
        sp = BeautifulSoup(resp.text, 'lxml')
        data_name += [i.text.strip() for i in sp.find_all(id='p_header')]
        data_article += [i.text.split()[1] for i in sp.find_all(class_='article')]
        data_price += [i.text.strip() for i in sp.find_all(id='price')]
        data_old_price += [i.text.strip() for i in sp.find_all(id='old_price')]
        data_descr += func([i for i in sp.find_all(id='description')])
        data_stock += [i.text.split(':')[1].strip() for i in sp.find_all(id='in_stock')]


    
    
    # 3_______________________________________________________________________________
    
    
columns = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса', 
           'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром']

data_lincs = list(map(lambda x: 'https://parsinger.ru/html/' + x, data_lincs))

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(columns)
    writer.writerows([[n]+[a]+d+[s]+[p]+[o]+[l] for n, a, d, s, p, o, l in zip(data_name, data_article, data_descr, data_stock, data_price, data_old_price, data_lincs)])
