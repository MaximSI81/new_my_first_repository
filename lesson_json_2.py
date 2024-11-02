# Импортируем необходимые библиотеки
import json
import requests
from bs4 import BeautifulSoup

# Создаём списки куда будем складывать данные
data_name = []
data_price = []
data_old_price = []
data_descr = []
data = []
data_links = []
data_art = []
data_count = []
# Цикл для перебора категорий товаров
for index in range(1, 6):
    # Вложенный цикл для перебора страниц товаров
    for page in range(1, 5):
        # Создаём сессию
        url = f'https://parsinger.ru/html/index{index}_page_{page}.html'
        session = requests.Session()
        response = session.get(url=url)
        response.encoding = 'utf-8'
        # Проверяем статус запроса
        if response:
            # Создание объекта BeautifulSoup для получения 'Link'
            soup = BeautifulSoup(response.text, 'lxml')
            links = [f'https://parsinger.ru/html/{a.find(["a"])["href"]}' for a in soup.find_all(class_='img_box')]
            # Проходим циклом по ссылкам на каждой странице
            for l in links:
                # Собираем 'Link' в список
                data_links.append(l)
                # Создаём сессию
                session_l = requests.Session()
                resp = session_l.get(l)
                resp.encoding = 'utf-8'
                # Проверяем статус запроса
                if resp:
                    # Создание объекта BeautifulSoup и собираем данные в каждой карточке
                    soup = BeautifulSoup(resp.text, 'lxml')
                    data_name.append(soup.find(id="p_header").text.strip())
                    data_price.append(soup.find(id='price').text.strip())
                    data_old_price.append(soup.find(id='old_price').text.strip())
                    data_art.append(soup.find(class_='article').text.split(': ')[1].strip())
                    data_descr.append(
                        {d['id']: d.text.split(': ')[1].strip() for d in soup.find(id='description').find_all('li')})
                    data_count.append(soup.find(id='in_stock').text.split(': ')[1].strip())
                else:
                    # Выводим статус запрос при возникновении ошибки
                    print(f'Что-то пошло не так: {resp.status_code}')

        else:
            # Выводим статус запрос при возникновении ошибки
            print(f'Что-то пошло не так: {response.status_code}')

# Проходим циклом по спискам, создаём словари по каждой карточке
for n, a, d, c, p, o, li in zip(data_name, data_art, data_descr, data_count, data_price, data_old_price, data_links):
    data.append({
        "categories": li.split('/')[-3],
        "name": n,
        "article": a,
        "description": d,
        "count": c,
        "price": p,
        "old_price": o,
        "link": li
    })
# Создаём и записываем данные в json файл
with open('res.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
