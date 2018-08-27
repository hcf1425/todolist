from flask import render_template
from flask_script import Manager
from apps import create_app

app = create_app()

# 创建脚本管理器对象
manager= Manager(app)



if __name__ == '__main__':
    print(app.url_map)
    manager.run()