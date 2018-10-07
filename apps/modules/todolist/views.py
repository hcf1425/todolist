from . import todo_blue
from flask import render_template
from flask import current_app

@todo_blue.route('/')
def index():

    context ={
        'user':None
    }
    return render_template('demo.html',context=context)


@todo_blue.route("/favicon.ico")
def title_icon():
    """
    返回网站图标
    :return: favicon.ico
    """
    return current_app.send_static_file("images/favicon.ico")