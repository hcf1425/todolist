from datetime import  datetime
from werkzeug.security import generate_password_hash,check_password_hash

from apps import db
from apps.utils import constants


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

class Users(BaseModel,db.Model):
    """用户模型"""
    __tablename__ = 'tb_users'

    id = db.Column(db.Integer,primary_key=True)     # 用户编号
    nick_name = db.Column(db.String(32),unique=True,nullable=False) # 用户昵称
    password_hash = db.Column(db.String(128),nullable=False)  # 用户密码
    mobile = db.Column(db.String(11),unique=True,nullable=False) # 手机号
    avatar_url = db.Column(db.String(256)) # 头像路径
    last_login =  db.Column(db.DateTime,default=datetime.now()) # 最后一次登录时间
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 用户性别
        db.Enum(
            'MAN',
            'WOMAN'
        )
    )

    tasks = db.relationship("Tasks", backref='user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        """
        校验用户名和密码是否正确
        :param password: 接受用户输入的密码明文
        :return: 返回校验结果， True or False
        """
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
            "mobile": self.mobile,
            "gender": self.gender if self.gender else "MAN",
            "signature": self.signature if self.signature else "",
            "tasks": self.tasks.title
        }
        return resp_dict


class Tasks(BaseModel,db.Model):
    """任务模型"""
    __tablename__ ='tb_tasks'

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    status = db.Column(db.Integer, default=0)  # 1 ：已完成 0：未完成
    user_id = db.Column(db.Integer, db.ForeignKey("tb_users.id"))
