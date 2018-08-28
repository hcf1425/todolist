from . import todo_blue
from flask import render_template

@todo_blue.route('/')
def index():

    context ={
        'user':None
    }
    return render_template('demo.html',context=context)