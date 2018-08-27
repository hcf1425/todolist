from flask import Flask,render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# 创建脚本管理器对象
manager= Manager(app)

class Config(object):
    """app配置类"""
    # 配置mysql数据库:指定数据库位置
    SQLALCHEMY_DATABASE_URI = "mysql://laowang:1@127.0.0.1:3306/todolist"

    # 禁用追踪msyql:因为mysql数据库性能差，如果再去追踪mysql所有修改，会再次浪费性能
    SQLALCHEMY_TTACK_MODIFICATIONS = False

# app加载配置
app.config.from_object(Config)

# 配置mysql数据库
db = SQLAlchemy(app)


@app.route('/',methods=["get",'post'])
def index():
    return render_template('todolist.html')

if __name__ == '__main__':
    manager.run()