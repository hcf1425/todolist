from . import task_blue
from flask import request,session,jsonify
from apps.utils.models import Users,Tasks
from apps.utils import response_code
from apps import db
import logging


@task_blue.route('/add',methods=["post"])
def add():

    json_dict = request.json
    task_name = json_dict.get('task')

    user_id = session.get('user_id')

    try:
        user = Users.query.filter(Users.id == user_id)
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户数据库查询异常")
    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户不存在")


    try:
        task_is_exist = Tasks.query.filter(Tasks.title == task_name).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    if task_is_exist:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务已经存在！")

    task = Tasks()
    task.title = task_name
    task.user_id = user_id

    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='数据库异常')

    # 5.响应添加任务成功
    return jsonify(errno=response_code.RET.OK, errmsg='添加任务成功')

