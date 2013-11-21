# -*- coding: utf8-*-
import smtplib
from email.mime.text import MIMEText

def send_mail(content, receiver='huaxingtan@yeah.net'):
    mail_host = 'smtp.163.com'
    mail_user = 'huaxingtan@163.com'
    mail_pwd = 'hxt94great!'
    mail_to = receiver

    msg = MIMEText(content.encode('utf-8'),'html', 'utf-8')
    msg['From'] = mail_user
    msg['Subject'] = '请法宝'
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        #login
        s.login(mail_user,mail_pwd)

        #send mail
        s.sendmail(mail_user,[mail_to],msg.as_string())
        s.close()
        print 'success'
    except Exception ,e:
        print e

