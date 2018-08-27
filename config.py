from flask_sqlalchemy import SQLAlchemy

class Config(object):
    """app配置类"""
    # 配置mysql数据库:指定数据库位置
    SQLALCHEMY_DATABASE_URI = "mysql://laowang:!@127.0.0.1:3306/todolist"

    # 禁用追踪msyql:因为mysql数据库性能差，如果再去追踪mysql所有修改，会再次浪费性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

