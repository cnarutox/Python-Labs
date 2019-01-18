from smtplib import SMTP

emails = []
with open('email.txt') as f:
    for line in f.readlines():
        try:
            if len(line.split()) > 1:
                emails.append(line.split()[1])
            else:
                emails.append(line.split()[0])
        except IndexError:
            continue

who = 'cx5128176@126.com'
body = f'''
From: {who}
To: {who}
Subject: Happy exam weeks!
Dear teacher,
Wish you can spend a wonderful exam weeks!

'''

sendSvr = SMTP('smtp.126.com')
sendSvr.login('cx5128176@126.com', 'passsowrd')
errs = sendSvr.sendmail(who, [who] + emails, body)
print(errs)
sendSvr.quit()
