from . import todo_blue
from flask import render_template

@todo_blue.route('/')
def index():

    return render_template('todolist.html')