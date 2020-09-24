# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/9 14:06
# software: PyCharm

"""
文件说明：

"""
from threading import Thread

from flask_mail import Message
from app import app, mail, settings


def send_async_email(app_, msg):
    with app_.app_context():
        mail.send(msg)


def send_email(recipients: list, username: str, pwd: str):
    msg = Message('找回密码：自然源订单生成器', sender=settings.Config.MAIL_USERNAME, recipients=recipients)
    msg.body = f'你的登录名：{username}，登录密码：{pwd}'
    with app.app_context():
        mail.send(msg)
    print('send email OK!')


def send_forget_password(emails: list, username, pwd):
    thread = Thread(target=send_email, args=[emails, username, pwd])
    thread.start()
    print('sending email')
