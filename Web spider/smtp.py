from smtplib import SMTP

emails = []
with open('email.txt') as f:
    for line in f.readlines():
        try:
            emails.append(line.split()[1])
        except IndexError:
            continue

who = 'cx5128176@126.com'
body = f'''
From: {who}
To: {who}
Subject: test msg

Hello World!
'''

sendSvr = SMTP('smtp.126.com')
sendSvr.login('cx5128176@126.com', '')
errs = sendSvr.sendmail(who, [who] + emails, body)
print(errs)
sendSvr.quit()