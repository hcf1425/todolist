from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

def create_app():

    app = Flask(__name__)

    # app加载配置
    app.config.from_object(Config)

    # 配置mysql数据库
    db = SQLAlchemy(app)
