import requests
import re
from bs4 import BeautifulSoup

with open(r'email.txt', 'a', encoding='utf-8') as f:
    # f.write('\n汉语言文化学院:\n')
    for i in range(2, 106):
        try:
            r = requests.get(
                f'http://hyxy.nankai.edu.cn/index.php/Home/Professor/professorShow/cid/6/uid/{i}'
            )
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find(attrs='ProfessorBasicInfo')
            name = info.li.string.strip()
            email = info.find_all('li')[-1].string.strip()
            if email == '':
                continue
            print(f'{i:3} {name:20}{email}')
            # f.write(f'{name:20}{email}\n')
        except Exception as e:
            print(e)
