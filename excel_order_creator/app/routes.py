# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/28 17:30
# software: PyCharm

"""
文件说明：

"""
import json
import os
from collections import OrderedDict
from datetime import datetime

from flask import request, render_template, redirect

from app import app
from app.goods_manager import goods_mgr
from app.plans_manager import plans_mgr
from writer.zry_order import ZRYOrder


def str_time():
    return datetime.now().strftime("%m%d %H_%M_%S")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('cart.html', good_list=goods_mgr.get_info_list(), plans_list=plans_mgr.get_plans())

    else:
        print(request.form.to_dict())

        params = request.form.to_dict()
        if not os.path.exists('orders') or not os.path.isdir('orders'):
            os.mkdir('orders')
        filename = f'{str_time()}.xlsx'
        excel = ZRYOrder(f'orders/{filename}')
        excel.write_table(params)
        excel.close()
        os.startfile('orders')
        return f'订单生成成功，请查看文件：{filename}'


@app.route('/init', methods=['GET', 'POST'])
def init():
    if request.method == 'GET':
        return render_template('init.html', good_list=goods_mgr.get_info_list(), good_count=len(goods_mgr.get_info_list()))

    else:
        params = request.form.to_dict()
        goods_mgr.save_price(params)
        return redirect('/')
    pass


@app.route('/plans', methods=['POST'])
def plans():
    params = request.form.to_dict()
    print(params)
    name = params.get("name")
    opt = params.get("opt")
    counts = params.get("counts")
    if opt == 'add':
        plans_mgr.add_plan(name, counts)
    elif opt == 'del':
        plans_mgr.del_plan(name)
    elif opt == 'mod':
        plans_mgr.mod_plan(name, counts)
    elif opt == 'use':
        return render_template('cart.html', good_list=goods_mgr.get_info_list(), plans_list=plans_mgr.get_plans(), plan_name=name)
    return redirect('/')

