import requests
import re
from bs4 import BeautifulSoup

with open(r'email.txt', 'a', encoding='utf-8') as f:
    # f.write('\n历史学院:\n')
    for i in range(1, 104):
        try:
            r = requests.get(
                f'http://history.nankai.edu.cn/main/t/info/121/{i}')
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find(attrs='info')
            name = info.find(attrs='name').string.strip()
            email = info.find(string=re.compile('Email：'))[7:].strip()
            if email == '':
                continue
            print(f'{i:3} {name:20}{email}')
            # f.write(f'{name:20}{email}\n')
        except Exception as e:
            print(e)
