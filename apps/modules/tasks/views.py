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


"""删除任务"""


@task_blue.route('/delete',methods=["post"])
def delete():
    json_dict = request.json
    task_name = json_dict.get('task_name')

    user_id = session.get('user_id')

    try:
        user = Users.query.filter(Users.id == user_id).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户数据库查询异常")
    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户不存在")
    try:
        task = Tasks.query.filter(Tasks.title == task_name).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    if task:
        db.session.delete(task)
        db.session.commit()

    # 5.响应添加任务成功
    return jsonify(errno=response_code.RET.OK, errmsg='删除任务成功')


"""上移任务"""

@task_blue.route('/up',methods=["post"])
def up():
    json_dict = request.json
    task_name = json_dict.get('task_name')

    user_id = session.get('user_id')

    try:
        user = Users.query.filter(Users.id == user_id).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户数据库查询异常")
    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户不存在")
    try:
        task_list = Tasks.query.filter(Tasks.user_id == user_id).all()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    try:
        task = Tasks.query.filter(Tasks.title == task_name).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    task_before = None

    for task_i in task_list:

        if task_i == task:
            break
        task_before = task_i

    if not task_before:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="已经是第一个了")

    task_before.title,task.title = task.title,task_before.title
    db.session.commit()

    return jsonify(errno=response_code.RET.OK, errmsg='上移任务成功')


@task_blue.route('/down',methods=["post"])
def down():
    json_dict = request.json
    task_name = json_dict.get('task_name')

    user_id = session.get('user_id')

    try:
        user = Users.query.filter(Users.id == user_id).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户数据库查询异常")
    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="用户不存在")
    try:
        task_list = Tasks.query.filter(Tasks.user_id == user_id).all()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    try:
        task = Tasks.query.filter(Tasks.title == task_name).first()
    except:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="任务数据库查询异常")

    task_after = None
    task_temp = None
    for task_i in task_list:

        if task_temp == task:
            task_after = task_i
            break
        task_temp = task_i

    if not task_after:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg="已经是最后一个了")

    task_after.title,task.title = task.title,task_after.title
    db.session.commit()

    return jsonify(errno=response_code.RET.OK, errmsg='下移任务成功')
