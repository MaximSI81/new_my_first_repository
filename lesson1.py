from bs4 import BeautifulSoup
import requests
import lxml
from random import choice

with open('user_agent.txt') as f:
    agent = f.readlines()
    headers = {'user_agent': choice(agent).strip(), 'x-requested-with': 'XMLHttpRequest'}

params = {'GiveName': 'Cardano', 'GetName': 'RUB', 'Sum': 100, 'Direction': 0}

url = f'https://bitality.cc/Home/GetSum?'

session = requests.Session()
response = session.get(url=url, headers=headers, params=params).json()

print(response)