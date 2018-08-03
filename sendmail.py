#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'yangb92@tom.com'
receivers = ['523084685@qq.com']

mail_host = 'smtp.tom.com'
mail_user = 'yangb92@tom.com'
mail_pwd = 'Admin1992'

def sendmail(title,content):
    message = MIMEText(content,'html','utf-8')
    message['From'] = Header('yangb92','utf-8')
    message['To'] = Header('master','utf-8')     
    message['Subject'] = Header(title,'utf-8')   
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pwd)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error:", e) 


if __name__ == '__main__':
    sendmail('我是python','你好,我会给你发送测试信息')
