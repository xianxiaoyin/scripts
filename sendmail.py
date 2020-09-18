'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-08-03 09:23:14
LastEditTime: 2020-09-18 10:53:24
'''
#!python3
# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

'''
简单的发送邮件脚本在py3测试通过
SendMail(content='邮件正文内容', subjuet='邮件标题', to=['收件人邮箱',''])
'''

class SendMail(object):
    def __init__(self, content, subjuet, to=None, cc=None):
        if to is None:
            to = []
        if cc is None:
            cc = []
        self.from_add = 'xxx@qq.com'
        self.smtp_server = 'smtp.163.com'
        self.to = to
        self.cc = cc
        self.content = content
        self.subject = subjuet

    def _headerConstruct(self, message):
        message['Subject'] = Header(self.subject, 'utf-8')
        message.add_header('To', ','.join(self.to))
        message.add_header('Cc', ','.join(self.cc))
        return message

    # 发送单个邮件
    def sends(self):
        messages = MIMEText(self.content, 'plain', 'utf-8')
        message = self._headerConstruct(messages)
        try:
            smtpObj = smtplib.SMTP(self.smtp_server, 25)
            smtpObj.sendmail(self.from_add, self.to, message.as_string())
            print('email send successful !')
        except Exception as e:
            print(e)
            print('email send fail !')

    # 发送带附件的邮件
    def sendAnnex(self, filename, filename2):
        messages = MIMEMultipart()
        message = self._headerConstruct(messages)

        # 构造附件1
        with open(filename, 'rb') as f:
            att1 = MIMEText(f.read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename)
        # 构造附件2
        with open(filename2, 'rb') as f2:
            att2 = MIMEText(f2.read(), 'base64', 'utf-8')
            att2["Content-Type"] = 'application/octet-stream'
            att2["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename2)
        message.attach(att1)
        message.attach(att2)

        try:
            smtpObj = smtplib.SMTP(self.smtp_server, 25)
            smtpObj.sendmail(self.from_add, self.to +
                                self.cc, message.as_string())
            print('email send successful !')
        except Exception as e:
            print(e)
            print('email send fail !')


if __name__ == '__main__':
    fileName = '1.txt'
    fileName2 = '2.txt'
    sendMail_to =['siweix.zhou@intel.com']
    sendMail_cc = []
    
    SendMail(content='', subjuet='this is title', to=sendMail_to, cc=sendMail_cc).sendAnnex(filename=fileName,filename2=fileName2)