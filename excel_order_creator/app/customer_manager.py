# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/8 15:01
# software: PyCharm

"""
文件说明：

"""
import json
import os


class CustomerManager(object):
    _customer_file = 'customer.json'
    customers = dict()

    def __init__(self):
        self.load()

    def load(self) -> dict:
        if os.path.exists(self._customer_file):
            with open(self._customer_file, encoding='utf-8') as f:
                data = f.read()
                if data:
                    self.customers = json.loads(data)
        return self.customers

    def save(self):
        with open(self._customer_file, 'w') as f:
            f.write(json.dumps(self.customers))

    def add(self, name, params: dict):
        print(self.customers)
        self.customers[params.get("sf_company")] = params
        print(self.customers)
        self.save()

    def del_(self, name):
        try:
            self.customers.pop(name)
            self.save()
        except KeyError:
            pass

    def mod(self, name, counts: list):
        self.customers[name] = counts
        self.save()

    def get(self, name=None):
        if name:
            p = self.customers.get(name)
            return p
        return self.customers.keys()


customer_mgr = CustomerManager()

