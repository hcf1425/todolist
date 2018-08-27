from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

# 全局变量db
db = SQLAlchemy()
# 准备一个空的redis_store
#redis_store = None  # type: StrictRedis
redis_store: StrictRedis = None

def create_app():

    app = Flask(__name__)

    # app加载配置
    app.config.from_object(Config)

    # 配置mysql数据库
    # db = SQLAlchemy(app)
    db.init_app(app)

    # 配置Redis
    global redis_store
    redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    from apps.modules.todolist import todo_blue
    app.register_blueprint(todo_blue)

    return app
