import threading

from flask import Flask
from flask_mail import Mail, Message
from app import mail
# from manage import app
# from app import mail
# import app.constants
import config

# #email address of sender
# MAIL_SERVER = "stmp.qq.com"
# MAIL_PORT ="465"
# MAIL_USE_SSL = True
# MAIL_USERNAME = '729823753@qq.com'
# MAIL_PASSWORD = 'zxbyjudgnuplbfaj'
# MAIL_SUPPRESS_SEND = '729823753@qq.com'


# app = Flask(__name__)
#
#
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'jikaisong1997@gmail.com'
# app.config['MAIL_PASSWORD'] = 'mvmsdleqfadzujxw'
# app.config.update(
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_PROT='587',
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME = 'jikaisong1997@gmail.com',
#     MAIL_PASSWORD = 'bjuptolgisabncup',
#     MAIL_DEFAULT_SENDER = 'jikaisong1997@gmail.com'
# )

mail = Mail(app)
@app.route("/")
def index():
    # send_mail()
    msg = Message("Hi!This is a test ",sender="jikaisong1997@gmail.com",recipients=['710881494@qq.com'])
    msg.body = "This is a first email"
    mail.send(msg)
    return "Sent"

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail():
    msg = Message("Hi!This is a test ",sender="729823753@qq.com" ,recipients=['710881494@qq.com.com'])
    msg.body = "This is a first email"
    #     with app.open_resource("F:\2281393651481.jpg") as fp:
    #         msg.attach("image.jpg", "image/jpg", fp.read())
    thr = threading.Thread(target =send_async_email, args = [app,msg])
    thr.start()

if __name__ == "__main__":
    app.run()
