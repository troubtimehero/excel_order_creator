# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/5 17:36
# software: PyCharm

"""
文件说明：

"""
import json
import os


class PlansManager(object):
    _plans_file = 'plans.json'
    plans = dict()

    def __init__(self):
        self.load_plans()

    def load_plans(self) -> dict:
        if os.path.exists(self._plans_file):
            with open(self._plans_file, encoding='utf-8') as f:
                data = f.read()
                if data:
                    self.plans = json.loads(data)
        return self.plans

    def save(self):
        with open(self._plans_file, 'w') as f:
            f.write(json.dumps(self.plans))

    def add_plan(self, name, counts: list):
        self.plans[name] = counts
        self.save()

    def del_plan(self, name):
        try:
            self.plans.pop(name)
            self.save()
        except KeyError:
            pass

    def mod_plan(self, name, counts: list):
        self.plans[name] = counts
        self.save()

    def get_plans(self) -> dict:
        dic = dict()
        for k, v in self.plans.items():
            dic[k] = v.split(',')
        return dic


plans_mgr = PlansManager()

