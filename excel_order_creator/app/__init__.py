# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/28 17:31
# software: PyCharm

"""
文件说明：

"""

from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy


# from settings import Config

# 创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)

# 添加配置信息
# app.config.from_object(Config)

# db = SQLAlchemy(app)

# migrate = Migrate(app, db)

from app import routes
