from flask import Blueprint

#用户认证蓝本

auth = Blueprint('auth',__name__)

from . import routes