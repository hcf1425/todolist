from . import todo_blue
from flask import render_template
from flask import current_app,session
from apps.utils.models import Users

@todo_blue.route('/')
def index():
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = Users.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    context = {
        'user': user.to_dict() if user else None
    }

    return render_template('demo.html',context=context)


@todo_blue.route("/favicon.ico")
def title_icon():
    """
    返回网站图标
    :return: favicon.ico
    """
    return current_app.send_static_file("images/favicon.ico")