
import json
import requests
from bs4 import BeautifulSoup

data_name = []
data_price = []
data_old_price = []
data_descr = []
data = []
data_links = []
data_art = []
data_count = []

for page in range(1, 5):
    url = f'https://parsinger.ru/html/index2_page_{page}.html'
    session = requests.Session()
    response = session.get(url=url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'lxml')
    links = [f'https://parsinger.ru/html/{a.find(["a"])["href"]}' for a in soup.find_all(class_='img_box')]
    for l in links:
        data_links.append(l)
        session_l = requests.Session()
        resp = session_l.get(l)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        data_name.append(soup.find(id="p_header").text.strip())
        data_price.append(soup.find(id='price').text.strip())
        data_old_price.append(soup.find( id='old_price').text.strip())
        data_art.append(soup.find(class_='article').text.split(': ')[1].strip())
        data_descr.append({d['id']: d.text.split(': ')[1].strip() for d in soup.find(id='description').find_all('li')})
        data_count.append(soup.find(id='in_stock').text.split(': ')[1].strip())

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

with open('res.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)