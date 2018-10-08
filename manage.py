from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from apps import create_app,db
from apps.utils import models  #这句话不能注释，否则迁移的时候会找不到模型类。报 no change detected


app = create_app()

# 创建脚本管理器对象
manager= Manager(app)

# 迁移时让app和db建立关联
Migrate(app,db)
# 把迁移脚本命令添加到脚本管理器对象
# 参数1  ： 表示别名,写个'hehe'都可以；参数2：迁移命令
manager.add_command("db",MigrateCommand)


if __name__ == '__main__':
    print(app.url_map)
    manager.run()