from flask import Blueprint

task_blue = Blueprint("tasks",__name__,url_prefix="/task")

from . import views