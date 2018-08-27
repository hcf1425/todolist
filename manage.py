from flask import render_template
from flask_script import Manager
from apps import create_app

app = create_app()

# 创建脚本管理器对象
manager= Manager(app)


@app.route('/',methods=["get",'post'])
def index():
    return render_template('todolist.html')

if __name__ == '__main__':
    manager.run()