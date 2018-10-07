from . import passport_blue
from flask import request,abort,make_response
from utils.captcha.captcha import captcha
import logging
from apps import redis_store
from apps.utils import constants

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