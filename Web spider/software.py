import requests
import re
from functools import reduce
from bs4 import BeautifulSoup


def extract(soup):
    for teacher in soup.find_all(attrs='span9')[1:]:
        # teacher = BeautifulSoup(teacher, 'html.parser')
        name = teacher.a.contents[0].strip()
        mail1, mail2 = [], []
        emails = teacher.find(attrs='cloaked_email')('span')
        # print(teacher.find(attrs='cloaked_email').prettify())
        for email in emails:
            r = re.match(r'^<span data-ep-\w+="(.*?)"\s+data-ep-\w+="(.*?)">',
                         str(email))
            mail1.append(r.group(1))
            mail2.insert(0, r.group(2))
        mail = reduce(lambda x, y: x + y, mail1 + mail2)
        print(name, mail)
    page = soup.find(title='下页')
    if page:
        print('http://cs.nankai.edu.cn' + page.get('href'))
        r = requests.get('http://cs.nankai.edu.cn' + page.get('href'))
        soup = BeautifulSoup(r.text, 'html.parser')
        extract(soup)


r = requests.get(
    'http://cs.nankai.edu.cn/index.php/zh/2017-01-15-22-19-36/2017-01-15-22-20-52'
)
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())
extract(soup)

# r = requests.get('http://www.nankai.edu.cn/213/list.htm')
# nankai = BeautifulSoup(r.text, 'html.parser')
# # print(nankai.prettify())
# for college in nankai.find_all(attrs={'tb_line tb_even'}):
#     name = college.a.string
#     url = college.a.get('href')
#     print(name, url)
# r = requests.get(url)
# college = BeautifulSoup(r.text, 'html.parser')
