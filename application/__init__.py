from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
#邮件
mail = Mail()

#数据库
db = SQLAlchemy()


#用户登陆管理
loginManger = LoginManager()
loginManger.session_protection = 'strong'
loginManger.login_view = 'auth.login'

#markdown模块
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)

    #初始化配置
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    #初始化mail 
    mail.init_app(app)

    #初始化db 
    db.init_app(app)

     #初始化loginmanager
    loginManger.init_app(app)

    #初始化markdown
    pagedown.init_app(app)


    #注册main蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    #注册auth蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app