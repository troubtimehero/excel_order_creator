# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/5 9:25
# software: PyCharm

"""
文件说明：

"""
import json
from app.win_tips import tips_only

settings = dict()


with open('settings.json', encoding='utf-8') as f:
    data = f.read()
    settings.update(json.loads(data))


def get_setting(ls: list):
    res = settings
    for i in ls:
        res = res.get(i, None)
        if res is None:
            tips_only('->'.join(ls), f'设置文档缺少参数')
            break
    return res
