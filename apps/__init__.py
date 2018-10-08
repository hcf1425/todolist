from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from logging.handlers import RotatingFileHandler
import pymysql,logging
pymysql.install_as_MySQLdb()

# 创建一个空的db对象
db = SQLAlchemy()
# 准备一个空的redis_store
redis_store = None
# redis_store: StrictRedis = None


def setup_log():
    # 设置日志的记录等级
    logging.basicConfig(level=logging.WARNING)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

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

    from apps.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    from apps.modules.tasks import task_blue
    app.register_blueprint(task_blue)

    return app
