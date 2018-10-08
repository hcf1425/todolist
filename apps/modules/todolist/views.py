from . import todo_blue
from flask import render_template
from flask import current_app,session
from apps.utils.models import Users,Tasks

@todo_blue.route('/')
def index():
    user_id = session.get('user_id')
    user = None
    tasks = []
    task_list = []

    if user_id:
        try:
            user = Users.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)


        try:
            task_list = Tasks.query.filter(Tasks.user_id==user_id)
        except:
            current_app.logger.error(e)

        for task in task_list:
            tasks.append(task.title)

    context = {
        'user': user.to_dict() if user else None,
        'tasks': tasks if task_list else None
    }

    return render_template('demo.html',context=context)


@todo_blue.route("/favicon.ico")
def title_icon():
    """
    返回网站图标
    :return: favicon.ico
    """
    return current_app.send_static_file("images/favicon.ico")