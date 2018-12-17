#!python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''
简单的发送邮件脚本在py3测试通过
SendMail(content='邮件正文内容', subjuet='邮件标题', to=['收件人邮箱',''])
'''

class SendMail(object):
    def __init__(self, content, subjuet, to=[]):
        self.from_add = '发件人邮箱'
        self.smtp_server = '发送邮件要使用的smtp服务器地址'
        self.to = to
        self.content = content
        self.subject = subjuet
        self.sends()

    def sends(self):
        message = MIMEText(self.content, 'plain', 'utf-8')
        message['Subject'] = Header(self.subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP(self.smtp_server, 25)
            smtpObj.sendmail(self.from_add, self.to, message.as_string())
            print('email send successful !')
        except Exception as e:
            print(e)
            print('email send fail !')


if __name__ == '__main__':
    SendMail(content='邮件正文内容', subjuet='邮件标题', to=['收件人邮箱',''])
