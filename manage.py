from flask import Flask,render_template
from flask_script import Manager

app = Flask(__name__)


# 创建脚本管理器对象
manager= Manager(app)



@app.route('/',methods=["get",'post'])
def index():
    return render_template('todolist.html')

if __name__ == '__main__':
    manager.run()