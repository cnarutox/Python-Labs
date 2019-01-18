import requests
import re
from bs4 import BeautifulSoup

with open(r'email.txt', 'a', encoding='utf-8') as f:
    # f.write('\n环境科学与工程学院:\n')
    r = requests.get('http://env.nankai.edu.cn/shiziduiwu/')
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    for info in soup.find(attrs='fck').find_all('a'):
        try:
            name = info.string.strip()
            r = requests.get(info.get('href'))
            r.encoding = r.apparent_encoding
            teacher = BeautifulSoup(r.text,
                                    'html.parser').find(attrs='teacherC')
            email = re.search(
                r'\w[-\w\.]*(@|(\[at\]))((nankai.edu.cn)|(126.com))',
                teacher.get_text()).group()
            email = re.sub('\[at\]', '@', email).strip()
            if email == '':
                continue
            print(f'{name:20}{email}')
            # f.write(f'{name:20}{email}\n')
        except Exception as e:
            print(e)
