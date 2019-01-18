import requests
import re
from bs4 import BeautifulSoup

r = requests.get(r'https://www.autohome.com.cn/use/201811/925434.html')
soup = BeautifulSoup(r.text, 'html.parser')

print('Use bs:\t', soup.title.string)
print('Use re:\t', re.search('<title>(.*?)</title>', r.text).group(1), '\n')

print('Use bs:\t', soup.find(attrs='time').string.strip())
print(
    'Use re:\t',
    re.search(r'<span class="time">((.|\n)*?)</span>',
              r.text).group(1).strip(), '\n')

page = r'https://www.autohome.com.cn/2277/0/0-0-1-0/'
r = requests.get(page)
soup = BeautifulSoup(r.text, 'html.parser')
page = int(soup.find(attrs='page')('a')[-2].string)
for i in range(1, page + 1):
    print(f'PAGE {i}:')
    r = requests.get(r'https://www.autohome.com.cn/2277/0/0-0-' + str(i) +
                     '-0/')
    soup = BeautifulSoup(r.text, 'html.parser')
    for new in soup.find_all('h3'):
        print(new.a.string, '\thttps:' + new.a.get('href'))
