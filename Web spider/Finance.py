import requests
import re
from bs4 import BeautifulSoup

with open(r'email.txt', 'a', encoding='utf-8') as f:
    # f.write('\n金融学院:\n')
    r = requests.get(f'http://finance.nankai.edu.cn/f/teacher/teacher/qzjs')
    soup = BeautifulSoup(r.text, 'html.parser')
    for info in soup.find_all(attrs='shiziListBox'):
        try:
            name = info.find(attrs='lead color_nankai').string.strip()
            email = info.find(attrs='mailBox mailText').string.strip()
            if email == '':
                continue
            print(f'{name:20}{email}')
            # f.write(f'{name:20}{email}\n')
        except Exception as e:
            print(e)
