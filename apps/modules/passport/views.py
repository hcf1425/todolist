import re,random

from . import passport_blue
from flask import request, abort, make_response, jsonify,json
from utils.captcha.captcha import captcha
import logging
from apps import redis_store
from apps.utils import constants,response_code
from apps.lib.dysms_python.demo_sms_send import *

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
    print(sms_code)
    logging.debug(sms_code)
    # 调用阿里云接口发送验证码
    __business_id = uuid.uuid1()
    code_json = "{'code':"+sms_code+"}"
    res=json.loads(send_sms(__business_id, phone_number, "hcf1425", "SMS_145595939", code_json).decode())
    status = res.get('Code')
    print(res)

    if status != "OK":
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='短信发送失败')

    try:
        redis_store.set("SMS:"+phone_number,sms_code,constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.DATAERR, errmsg='存储短信失败')

    # 8.返回短信验证码发送的结果
    return jsonify(errno=response_code.RET.OK, errmsg='发送短信成功')

