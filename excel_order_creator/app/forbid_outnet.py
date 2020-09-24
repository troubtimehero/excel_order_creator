# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/12 13:21
# software: PyCharm

"""
文件说明：

"""
import json
import os


class ForbidOutNet(object):
    forbid = False
    _file = 'forbid.json'

    def __init__(self):
        self.forbid = self.load().get('forbid', False)

    def load(self) -> dict:
        if os.path.exists(self._file):
            with open(self._file, 'r') as f:
                data = f.read()
                if data:
                    dic = json.loads(data)
                    return dic
        return {}

    def save(self, fb):
        if self.forbid != fb:
            self.forbid = fb
            with open(self._file, 'w') as f:
                f.write(json.dumps({'forbid': self.forbid}))

    def get(self):
        return self.forbid


forbid_mgr = ForbidOutNet()

