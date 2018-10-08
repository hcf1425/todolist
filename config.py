from redis import StrictRedis

class Config(object):
    """app配置类"""
    DEBUG = True
    # 配置mysql数据库:指定数据库位置
    SQLALCHEMY_DATABASE_URI = "mysql://root:hcfhcf123@127.0.0.1:3306/todolist"

    # 禁用追踪msyql:因为mysql数据库性能差，如果再去追踪mysql所有修改，会再次浪费性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 秘钥
    SECRET_KEY = "HAJKHKJ"

    # 配置Session:将flask的session数据引导到redis
    SESSION_TYPE = "redis"  # 存储到redis
    # 配置redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 使用签名将session的明文转成密文
    SESSION_USE_SIGNER = True
    # 设置session有效期为一天
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24
