from flask import render_template,request,flash,redirect,url_for,session
from application.models import Users
from application import db
from flask_login import login_user,login_required,logout_user,current_user
from .forms import LoginForm,RegisterForm
from . import auth
from application.emails import send_email

#登陆/注册路由
@auth.route('/login',methods=["GET","POST"])
def login():
    # print(request.form)

    loginForm = LoginForm()
    registerForm = RegisterForm()

    if(loginForm.validate_on_submit()):
        print("loginForm.validate_on_submit")
        lemail = loginForm.lemail.data
        lpassword = loginForm.lpassword.data
        user = Users.query.filter_by(email=lemail).first()
        if(not user):
            flash("不存在该用户")
            return redirect(url_for(".login"))
        elif not user.check_password(lpassword):
            flash("密码错误")
            return redirect(url_for(".login"))
        else:
            flash("登陆成功")
            print("登陆成功")
            session['email'] = loginForm.lemail.data
            login_user(user,True)
            return redirect(request.args.get('next') or url_for("main.index") )
        # return redirect("/login")


    if(registerForm.validate_on_submit()):
        print("registerForm.validate_on_submit")
        rname        = registerForm.rname.data
        remail       = registerForm.remail.data
        rpassword    = registerForm.rpassword.data
        
        
        newuser =  Users(name=rname,email=remail)
        newuser.set_password(rpassword)
        db.session.add(newuser)
        db.session.commit()

        token = newuser.generate_confirmation_token()

        send_email(newuser.email,'验证账户','auth/email/confirm',user=newuser,token=token)
        flash("验证邮件已发送至您的邮箱")

        return redirect(url_for(".login"))

    loginForm.lemail.data = session.get('email')
    return render_template("auth/login.html",loginForm=loginForm,registerForm=registerForm)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("注销成功")
    return redirect(url_for('main.index'))

#验证路由
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    print("验证")
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        print("验证成功")
        flash('验证成功!')
    else:
        flash("验证链接错误")
        print("验证失败")
    return redirect(url_for('main.manage'))

#限制已注册登陆但未验证的用户
@auth.before_app_request
def before_request():
    if current_user.is_authenticated\
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.'\
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


#已注册登陆但未验证的用户看到的路由
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

# 重新发送验证邮箱路由
@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'验证账户','auth/email/confirm',user=current_user,token=token)
    flash("验证邮件已经重新发送")
    return redirect(url_for('auth.unconfirmed'))