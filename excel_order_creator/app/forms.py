# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/8 13:38
# software: PyCharm

"""
文件说明：

"""


class FormItem(object):
    def __init__(self, id_: str, placeholder: str):
        self.id_ = id_
        self.placeholder = placeholder


sell_form = [
    FormItem('sf_company', '收货单位'),
    FormItem('sf_tel', '电话'),
    FormItem('sf_customer', '客户'),
    FormItem('sf_address', '交货地址'),
    FormItem('sf_order_no', '订单编号'),
    FormItem('sf_salesman', '业务员'),
]
