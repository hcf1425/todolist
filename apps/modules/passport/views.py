import re,random,datetime

from . import passport_blue
from flask import request, abort, make_response, jsonify,json,session
from utils.captcha.captcha import captcha
import logging
from apps import redis_store,db
from apps.utils import constants,response_code
from apps.lib.dysms_python.demo_sms_send import *
from apps.utils.models import Users


@passport_blue.route('/login')
def login():
    return "hello world"


"""图片验证码逻辑实现"""


@passport_blue.route("/image_code")
def get_image_code():
    """
    :return:
    """
    # 1.接受参数
    image_code_id = request.args.get('imageCodeID')

    # 2.校验参数
    if not image_code_id:
        abort(400)  # 缺少参数

    # 3.生成图片及验证码
    name,text,image = captcha.generate_captcha()

    try:
        redis_store.set("imageID:"+image_code_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        logging.error(e)
        abort(500)

    response = make_response(image)

    response.headers["Content-Type"] = "image/jpg"
    return response


"""短信验证码发送业务逻辑"""


@passport_blue.route('/sms_code',methods =["post"])
def send_sms_code():

    # 1.获取数据
    print(request)
    json_dict = request.json
    print(json_dict)
    phone_number =json_dict.get('mobile')
    client_image_code = json_dict.get("image_code")
    image_code_id =json_dict.get("image_code_id")

    # 2.检验数据
    if not all([phone_number,client_image_code,image_code_id]):
        return jsonify(errno = response_code.RET.PARAMERR,errmsg = "缺少必传参数")
    if not re.match("^1[3-8]\d{9}$",phone_number):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="电话号码有误")
    try:
        server_image_code = redis_store.get("imageID:"+image_code_id)

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.DBERR, errmsg='查询图片验证码失败')

    if not server_image_code:
        return jsonify(errno=response_code.RET.NODATA, errmsg='图片验证码不存在')

    if client_image_code.lower() != server_image_code.lower():
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='验证码输入有误')

    sms_code = "%06d" % random.randint(0,999999)
    # print(sms_code)
    logging.debug(sms_code)
    # 调用阿里云接口发送验证码
    __business_id = uuid.uuid1()
    code_json = "{'code':"+sms_code+"}"
    res=json.loads(send_sms(__business_id, phone_number, "hcf1425", "SMS_145595939", code_json).decode())
    status = res.get('Code')
    # print(res)

    if status != "OK":
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='短信发送失败')

    try:
        redis_store.set("SMS:"+phone_number,sms_code,constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.DATAERR, errmsg='存储短信失败')

    # 8.返回短信验证码发送的结果
    return jsonify(errno=response_code.RET.OK, errmsg='发送短信成功')


"""注册业务逻辑"""


@passport_blue.route('/register',methods=["POST"])
def register():
    # 1.接受参数
    print("正在注册..............")
    json_dict =request.json
    phone_num = json_dict.get("mobile")
    client_sms_code = json_dict.get("smscode")
    password = json_dict.get("password")

    # 2. 校验参数
    if not all([phone_num,client_sms_code,password]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数不完整')

    try:
        server_sms_code = redis_store.get("SMS:"+phone_num)

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='数据库查询异常')

    if client_sms_code.lower() != server_sms_code.lower():
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='验证码输入有误')

    # 3.进行注册，将用户数据记录到数据
    user = Users()
    user.mobile = phone_num
    user.nick_name = phone_num
    user.password = password

    # 记录用户登录时间
    user.last_login = datetime.datetime.now()

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='数据库异常')


    # 4.状态保持
    session["user_id"] = user.id

    # 5.响应注册成功
    return jsonify(errno=response_code.RET.OK, errmsg='注册成功')


"""退出登录后端逻辑"""


@passport_blue.route("/logout")
def logout():
    """
    退出登录
    """
    # 清理session数据

    session.pop("user_id",None)
    session.pop("mobile", None)
    session.pop("nick_name", None)
    # 逻辑优化：如果是管理员身份进入到前台，退出前台时，需要将is_admin清除
    session.pop("is_admin",False)

    return jsonify(errno=response_code.RET.OK, errmsg='退出登录成功')


"""登录逻辑"""


@passport_blue.route("/login",methods =["POST"])
def login_user():
    # 1.接收数据
    json_dict = request.json
    phone_number = json_dict.get("mobile")
    password = json_dict.get("password")

    # 2、校验参数
    if not all([phone_number,password]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='参数不完整')

    # 3、使用手机号查询用户信息
    user = None
    try:
        user = Users.query.filter(Users.mobile == phone_number).first()

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='数据库查询异常！')

    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户名或密码输入有误！1')
    # if user.password_hash != password:
    #     return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户名或密码输入有误！')
    # pass

    # 4、匹配该用户要登录的用户密码
    if not user.check_password(password):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户名或密码输入有误！2')

    # 5、记录最后一次登录时间
    user.last_login =datetime.datetime.now()
    try:
        # 修改数据不用add()
        db.session.commit()

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户最近一次登录时间记录异常')

    # 6、状态保持
    session["user_id"] = user.id
    # session["mobile"] = user.mobile
    # session["nick_name"] = user.nick_name

    # 7、响应结果
    return jsonify(errno=response_code.RET.OK, errmsg='登录成功')