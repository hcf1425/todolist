from flask import Blueprint

todo_blue = Blueprint('todo',__name__)

from . import views