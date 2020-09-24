# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/28 17:30
# software: PyCharm

"""
文件说明：

"""
import json
import os
from datetime import datetime, timedelta
from queue import Queue

from flask import request, render_template, redirect, send_from_directory, session, flash

from app import app, db
from app.customer_manager import customer_mgr
from app.forbid_outnet import forbid_mgr
from app.forms import sell_form
from app.goods_manager import goods_mgr
from app.modles import valid_register, User, find_forget, valid_login, BOSS
from app.plans_manager import plans_mgr
from writer.zry_order import ZRYOrder

from app.send_email import send_forget_password


def str_time():
    return datetime.now().strftime("%m%d_%H_%M_%S")


_excel_dir = 'orders'
_file_queue = Queue()

if not os.path.exists(_excel_dir) or not os.path.isdir(_excel_dir):
    os.mkdir(_excel_dir)
else:
    for x in os.listdir(_excel_dir):
        os.remove(os.path.join(_excel_dir, x))


def put_new_file(filepath):
    while _file_queue.qsize() >= 5:
        os.remove(_file_queue.get())
    _file_queue.put(filepath)


def is_can_access():
    user, inner = valid_login(session.get('user'), session.get('password'))
    return user, inner == 1


@app.route('/order_creator/', methods=['GET', 'POST'])
def index():
    user, inner = is_can_access()
    if not user:
        return redirect("/order_creator/login")

    if request.method == 'GET':
        if inner:
            return render_template('cart.html',
                                   good_list=goods_mgr.get_info_list(),
                                   plans_list=plans_mgr.get_plans(),
                                   sell_form=sell_form,
                                   customers_list=customer_mgr.get(),
                                   logined=True
                                   )
        elif forbid_mgr.get():
            flash("该账号暂时无法登录")
            return redirect("/order_creator/login")
        else:
            return render_template('visitor.html',
                                   good_list=goods_mgr.get_info_list(),
                                   logined=True)

    else:
        # print(request.form.to_dict())

        params = request.form.to_dict()
        opt = params.get('opt')

        filepath = os.path.join(_excel_dir, f'{str_time()}.xlsx')
        with ZRYOrder(filepath) as excel:
            if opt == 'produce':
                excel.write_order_prod('生产单', params)
            elif opt == 'sell':
                excel.write_order_sell('销售单', params)
            else:
                excel.write_order_sell('销售单', params)
                excel.write_order_prod('生产单', params)

        put_new_file(filepath)
        # Todo: 放在服务器，就不打开文件夹了，而是要生成下载地址
        # os.startfile(path)
        # return f'{"生产" if opt == "produce" else "销售"}订单已生成，请查看文件：{path}/{filename}'
        return filepath.replace('\\', '/')


@app.route('/order_creator/init', methods=['GET', 'POST'])
def init():
    username = session.get('user')
    password = session.get('password')
    if username not in BOSS.keys() or username != 'boss':
        if valid_login(username, password)[0]:
            flash('修改价格，请以管理员身份登录')
        return redirect("/order_creator/login")

    if request.method == 'GET':
        return render_template('init.html', good_list=goods_mgr.get_info_list(), forbid=forbid_mgr.get(), logined=True)

    params = request.form.to_dict()
    goods_mgr.save_price(params)
    return redirect('/order_creator')


@app.route('/order_creator/plans', methods=['POST'])
def plans():
    params = request.form.to_dict()
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
        return json.dumps(plans_mgr.get_plans(name))
    return redirect('/order_creator')


@app.route('/order_creator/customer', methods=['POST'])
def customer():
    params = request.form.to_dict()
    opt = params.get("opt")
    name = params.get("name")
    # todo:
    if opt == 'add':
        customer_mgr.add(name, params)
    elif opt == 'del':
        customer_mgr.del_(name)
    elif opt == 'mod':
        customer_mgr.mod(name, params)
    elif opt == 'use':
        return json.dumps(customer_mgr.get(name))
    return redirect('/order_creator')


@app.route('/order_creator/orders/<filename>', methods=['GET'])
def download(filename):
    path = os.path.join(os.getcwd(), 'orders')
    return send_from_directory(path, filename, as_attachment=True)


@app.route('/order_creator/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    name = request.form.get("username")
    password = request.form.get("password")
    if valid_login(name, password)[0]:
        session["user"] = name
        session['password'] = password
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=7)  # 设置session到期时间
        return redirect("/order_creator")
    else:
        return render_template('login.html', msg='账号或密码错误')


@app.route('/order_creator/logout', methods=["GET"])
def logout():
    session["user"] = ""
    session['password'] = ""
    return redirect("/order_creator/login")


def valid_email_format(email):
    import re
    c = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')
    s = c.search(email)
    return True if s else False


@app.route('/order_creator/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    # invite_code = request.form.get("invite_code")
    # print('name:{}, email:{}, password:{}, password2:{}'.format(name, email, password, password2))

    if not name or not email or not password or not password2:
        msg = "请把注册信息填写完整"
    elif not valid_email_format(email):
        msg = "请填写正确的邮箱"
    elif password != password2:
        msg = "密码不一致"
    elif valid_register(name, email):
        user = User(username=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect("/order_creator/login")
    else:
        msg = '该用户名或邮箱已被注册！'

    return render_template('register.html', msg=msg)


@app.route('/order_creator/forget', methods=["GET", "POST"])
def forget():
    if request.method == 'GET':
        return render_template('forget.html')

    email = request.form.get("email")

    if not email or not valid_email_format(email):
        msg = "请填写正确的邮箱"
    else:
        found, username, password = find_forget(email)
        if found:
            send_forget_password([email], username, password)
            flash("用户名及密码已发送至邮箱，请注意查收")
            return redirect("/order_creator/login")
        else:
            msg = "该邮箱未注册"

    return render_template('forget.html', msg=msg)


@app.route('/order_creator/forbid', methods=["POST"])
def forbid():
    print(request.form.to_dict())
    fb = request.form.get('forbid', 'no')
    forbid_mgr.save(True if fb == 'yes' else False)
    return ''

