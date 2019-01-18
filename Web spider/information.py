colleges = [[
    '文学院', 'http://wxy.nankai.edu.cn/People/Detail/{}/0',
    '''info = soup.find(attrs='basicInfo')
            name = info.h3.string.strip()
            email = info.find_all('p')[-1].string.strip()
            email = re.sub('\[a\]|#', '@', email).strip()
            email = re.sub('Email:|--|邮箱\d*：|;', '', email).strip()'''
], [
    '历史学院', 'http://history.nankai.edu.cn/main/t/info/121/{}'
    '''info = soup.find(attrs='info')
            name = info.find(attrs='name').string.strip()
            email = info.find(string=re.compile('Email：'))[7:].strip()'''
]]