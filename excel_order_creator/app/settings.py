# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/5 9:25
# software: PyCharm

"""
文件说明：

"""
import json
import os
from app.win_tips import tips_only


settings_sell = dict()
settings_produce = dict()

with open('settings_sell.json', encoding='utf-8') as f:
    print('read settings_sell.json')
    data = f.read()
    settings_sell.update(json.loads(data))

with open('settings_produce.json', encoding='utf-8') as f:
    print('read settings_produce.json')
    data = f.read()
    settings_produce.update(json.loads(data))


def get_cfg_sell(ls: list):
    res = settings_sell
    for i in ls:
        res = res.get(i, None)
        if res is None:
            tips_only('->'.join(ls), f'设置文档缺少参数')
            break
    return res


def get_cfg_prod(ls: list):
    res = settings_produce
    for i in ls:
        res = res.get(i, None)
        if res is None:
            tips_only('->'.join(ls), f'设置文档缺少参数')
            break
    return res


class Config(object):
    # 为了确保表单提交过来的是安全的，所以我们设定一个安全钥匙。
    SECRET_KEY = 'ZRY!2020.08-10*9hjas53^#nm#BBJ*k23x['
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data.sqlite').replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''      # 邮箱账号
    MAIL_PASSWORD = ''      # QQ邮箱授权码


HOST = "127.0.0.1"
PORT = "9527"

with open('config.json') as f:
    print('read config.json')
    data = f.read()
    if data:
        dic = json.loads(data)
        HOST = dic.get("HOST", HOST)
        PORT = dic.get("PORT", PORT)

        Config.MAIL_SERVER = dic.get("MAIL_SERVER", "")
        Config.MAIL_USERNAME = dic.get("MAIL_USERNAME", "")
        Config.MAIL_PASSWORD = dic.get("MAIL_PASSWORD", "")
        Config.MAIL_PORT = dic.get("MAIL_PORT", "")

