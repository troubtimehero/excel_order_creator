# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/9/9 9:39
# software: PyCharm

"""
文件说明：

"""


# 定义ORM
from app import db
from sqlalchemy import and_, or_


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    # usertype = db.Column(db.Integer)    # 1:内部人员，0:外部人员

    def __repr__(self):
        return '<User %r>' % self.username


BOSS = {"boss": "123zry321", "zry": "888888"}


# 登录检验（用户名、密码验证）
def valid_login(username, password) -> (bool, int):
    # print(username, password)
    if username in BOSS and BOSS[username] == password:
        return True, 1
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    return (True, 0) if user else (False, 0)


# 注册检验（用户名、邮箱验证）
def valid_register(username, email):
    if username in BOSS:
        return False
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    return False if user else True


# 找回密码检验（邮箱）
def find_forget(email) -> (bool, str, str):
    user = User.query.filter(User.email == email).first()
    if user:
        return True, user.username, user.password
    return False, None, None


# def get_inner_user() -> list:
#     users = User.query.filter(User.usertype == 1).all()
#     return list(users)
