import csv
import requests
from bs4 import BeautifulSoup

data_lincs = []
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
    
    data_lincs += [i.find('a')['href'] for i in soup.find_all(class_='img_box')]
    
    
    
    
    
    
    
    # 3_______________________________________________________________________________
    
    
columns = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса', 
           'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром']



print(data_lincs)