import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_key"

    #mysql:   mysql+pymysql://username:password@host/database
    #postgres: postgresql://username:password@host/database

    # SQLALCHEMY_DATABASE_URI = r"mysql+pymysql://root:1234@localhost/dam" #这里填写你自己的数据库,格式参考如上
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.qq.com" #邮箱域名
    MAIL_PORT = "587"   #邮箱监听端口
    MAIL_USE_TLS = True #默认
    MAIL_USERNAME = "" #发送邮箱号
    MAIL_PASSWORD = ""  #邮箱pip认证码
    MAIL_DEFAULT_SENDER = "" #默认发送者
    FLASKY_MAIL_SENDER = "中华器乐"  #发送者名字

class DevConfig(Config):
    CWY_TMP = "whatever"

config = {
    'develop' : DevConfig,
    'default' : Config
}

