import requests
import re
from bs4 import BeautifulSoup

# 文件读写可注释
with open(r'email.txt', 'w', encoding='utf-8') as f:
    # f.write('文学院:\n')
    for i in range(9, 150):
        try:
            r = requests.get(f'http://wxy.nankai.edu.cn/People/Detail/{i}/0')
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find(attrs='basicInfo')
            name = info.h3.string.strip()
            email = info.find_all('p')[-1].string.strip()
            email = re.sub('\[a\]|#', '@', email).strip()
            email = re.sub('Email:|--|邮箱\d*：|;', '', email).strip()
            if email == '':
                continue
            print(f'{i:3} {name:20}{email}')
            # f.write(f'{name:20}{email}\n')
        except Exception as e:
            print(e)
