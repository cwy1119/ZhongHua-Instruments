from application import mail
from flask_mail import Message
from flask import current_app,render_template
class VerifyMail:
    subject = "欢迎注册CWY的网站"
    def sendCode(self,receiver,code):
        body = "您的验证码为: "+code+"\n,请尽快输入且不要透露给其他人"
        message = Message(subject=self.subject,recipients=[receiver],body=body)
        try:
            mail.send(message)
            return True
        except Exception as e:
            return False

def send_email(to,subject,template,**kwargs):
    subject = "欢迎注册CWY的网站"
    body = render_template(template+".txt",**kwargs)
    message = Message(subject=subject,recipients=[to],body=body)
    try:
        mail.send(message)
        return True
    except Exception as e:
        return False
    # msg = Message(subject,sender=current_app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    # msg.body = render_template(template+".txt",**kwargs)
    # msg.html = render_template(template+".html",**kwargs)
    # mail.send(msg)
