import requests
import re
from bs4 import BeautifulSoup

with open(r'1.txt', 'a', encoding='utf-8') as f:
    f.write('\n商学院:\n')
    r = requests.get(f'http://bs.nankai.edu.cn/jstd/list.htm')
    soup = BeautifulSoup(r.text, 'html.parser')
    for i in range(1, 9):
        info = soup.find(attrs=f'wp_column column-3-{i} ')
        r = requests.get('http://bs.nankai.edu.cn' + info.a.get('href'))
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in range(1, 21):
            try:
                info = soup.find(attrs=f'list_item i{i}')
                name = info.div.find(attrs='Article_Title').text.strip()
                email = info.find(attrs='fields ex_fields').find(
                    attrs='Article_Field4').text.strip()
                if email == '' or name == '':
                    continue
                print(f'{name:20}{email}')
                f.write(f'{name:20}{email}\n')
            except Exception as e:
                print(e)
