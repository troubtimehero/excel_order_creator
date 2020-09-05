# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/29 17:20
# software: PyCharm

"""
文件说明：

"""
import json
import os


class GoodInfo(object):

    def __init__(self, type_, local_path, name, unit, price, rate):
        self.type_ = type_
        self.local_path = local_path
        self.name = name
        self.unit = unit
        self.price = price
        self.rate = rate

    def __repr__(self):
        return f'{self.name}, {self.price}, {self.rate}, {self.unit}'


class GoodsManager(object):
    _price_file = 'prices.json'
    good_info_list = list()

    def __init__(self):

        gi_dict = self.load_price()

        images_path = os.path.join(os.path.dirname(__file__), 'static/images')

        # 要列出当前目录下的所有目录，只需要一行代码：
        dirs = [x for x in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, x))]

        # 要列出所有的.py文件，也只需一行代码：
        image_types = dict()
        for _dir in dirs:
            image_types[_dir] = [x for x in os.listdir(os.path.join(images_path, _dir)) if os.path.isfile(os.path.join(images_path, _dir, x))]

        # 0:type, 1:local_path, 2:name, 3:price, 4:count, 5:sum
        for _type, images in image_types.items():
            for image in images:
                info = os.path.splitext(image)[0].split('，')
                if len(info) == 1:
                    info.append('')
                if len(info) == 2:
                    info.append('文件名未指定单位')
                pr = gi_dict.get(image)
                self.good_info_list.append(GoodInfo(_type,
                                                    f'images/{_type}/{image}',
                                                    f'{info[0]}\n{info[1]}' if info[1] else f'{info[0]}',
                                                    info[2],
                                                    pr[0] if pr else 0,
                                                    pr[1] if pr else 0))

    def load_price(self) -> dict:
        if os.path.exists(self._price_file):
            with open(self._price_file, 'r') as f:
                data = f.read()
                if data:
                    dic = json.loads(data)
                    return dic
        return {}

    def save_price(self, price_rate_dict: dict):
        for i, pr in price_rate_dict.items():
            index = int(i) - 1
            pr = pr.split(',')
            self.good_info_list[index].price, self.good_info_list[index].rate = pr[0], pr[1]

        dic = dict()
        for gi in self.good_info_list:
            dic[gi.local_path.split('/')[-1]] = [gi.price, gi.rate]

        with open(self._price_file, 'w') as f:
            f.write(json.dumps(dic))

    def get_info_list(self) -> list:
        return self.good_info_list


goods_mgr = GoodsManager()
