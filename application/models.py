from flask_login import UserMixin
from flask import current_app
from application import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime,time
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from . import loginManger

#用户数据模型
class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(8),nullable=True,unique=True)
    email = db.Column(db.String(50),nullable=True,unique=True)
    phone = db.Column(db.Integer,nullable=True,unique=True)
    pwd = db.Column(db.String(100),nullable=False)
    gender = db.Column(db.Enum('male','female'),nullable=True)
    age = db.Column(db.Integer,nullable=False,server_default = '18')
    regesiter_date = db.Column(db.DateTime,nullable=False,server_default=func.now())

    #注册时是否验证标志
    confirmed = db.Column(db.Boolean, default=False)

    #hash加密
    def set_password(self,password):
        self.pwd = generate_password_hash(password)

    #检查密码是否与hash值匹配
    def check_password(self,password):
        return check_password_hash(self.pwd,password)

    #生成验证时token
    def generate_confirmation_token(self,expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    #验证通过
    def confirm(self,token):
        s =  Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

# db.create_all()
@loginManger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#媒体资源的抽象父类,不对应数据库中的表
class Source(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(40),nullable=True)
    url = db.Column(db.String(40),nullable=False,unique=True)

    def __repr__(self):
        return '<Audio %r>'%self.name

    def get_id(self):
        return self.id

#音频资源表
class Audio(Source):
    __tablename__ = 'audio'


#图像资源表
class Image(Source):
    __tablename__ = 'image'

#乐器表
class Instruments(db.Model):
    __tablename__ = 'instruments'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(8),nullable=False,unique=True)
    title = db.Column(db.String(8),nullable=False,unique=True)
    intro = db.Column(db.Text)
    pic = db.Column(db.Integer,db.ForeignKey('image.id'))
    famouses = db.relationship('Famous')
    masterworks = db.relationship('Masterwork')
    gamuts = db.relationship('Gamut')
    #待完善

    def get_id(self):
        return self.id
    

#名人介绍
class Famous(db.Model):
    __tablename__ = 'famous'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    iid =  db.Column(db.Integer,db.ForeignKey('instruments.id'))
    name = db.Column(db.String(8),nullable=False,unique=True)
    pic = db.Column(db.Integer,db.ForeignKey('image.id'))
    comments = db.relationship('Comment')
    def get_id(self):
        return self.id
#名人注释
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    fid = db.Column(db.Integer,db.ForeignKey('famous.id'))
    title = db.Column(db.String(8))
    content = db.Column(db.Text)

#名曲
class Masterwork(db.Model):
    __tablename__ = 'masterwork'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    iid =  db.Column(db.Integer,db.ForeignKey('instruments.id'))
    mp3 = db.Column(db.Integer,db.ForeignKey('audio.id'))
    coverpic = db.Column(db.Integer,db.ForeignKey('image.id'))
    name = db.Column(db.String(15))
    title = db.Column(db.String(15))
    content = db.Column(db.Text)


#音节
class Gamut(db.Model):
    __tablename__ = 'gamut'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    iid =  db.Column(db.Integer,db.ForeignKey('instruments.id'))
    index = db.Column(db.Integer)
    note_c  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_db =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_d  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_eb =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_e  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_f  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_gb =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_g  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_ab =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_a  =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_bb =   db.Column(db.Integer,db.ForeignKey('audio.id'))
    note_b  =   db.Column(db.Integer,db.ForeignKey('audio.id'))