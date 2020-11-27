from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from application.models import Users

class LoginForm(FlaskForm):
    lemail = StringField("Email",validators=[DataRequired(),Email()])
    lpassword = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    # lremember_me = BooleanField("Remember Me")
    lsubmit = SubmitField("Login")

class RegisterForm(FlaskForm):
    rname = StringField("Name",validators=[DataRequired(),Length(max=8)])
    remail = StringField("Email",validators=[DataRequired(),Email()])
    rpassword = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    rpassword_confirm = PasswordField("Confirm Password",validators=[DataRequired(),Length(min=6,max=15),EqualTo("rpassword",message="两次输入的密码不一致")])
    rsubmit = SubmitField("Register")

    #检查remail字段,若存在就抛出错误(表单不符合要求)
    def validate_remail(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("邮箱已经被注册")

    #检查rname字段,若存在就抛出错误(表单不符合要求)
    def validate_rname(self,name):
        user = Users.query.filter_by(name = name.data).first()
        if user:
            raise ValidationError("昵称已存在")