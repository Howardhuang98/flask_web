# encoding: utf-8
import subprocess

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

import config
from decorators import login_required
from exts import db
from models import User, Message

app = Flask(__name__)
app.config.from_object(config)

#   app
#    | flask_sqlaichemy
#   ORM映射
#    |
#   数据库
# 将db对象与app对象进行关联
db.init_app(app)


# 主页，默认情况是不登陆无法进入
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        message = "致敬伟大的龚哥   G.O.A.T."
        return render_template('login.html', message=message)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password ==
                                 password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="登陆失败！")


@app.route('/index')
@login_required
def index():
    messages = Message.query.order_by(Message.create_time.desc()).limit(10).all()
    return render_template('index.html', messages=messages)


# 判断用户是否登录，只要我们从session中拿到数据就好了   注销函数
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('message.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        message = Message(title=title, content=content)
        user_id = session.get('user_id')
        message.author_id = user_id
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', message="请填写表单")
    else:
        username = request.form.get('username')
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        answer = request.form.get('answer')
        if password == repassword and answer == '罗斯':
            try:
                user = User(telephone=telephone, username=username, password=password, level=1)
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback
                return render_template('notification.html', notification="注册失败，数据库中已存在该用户或手机号", web='/register/')
            return render_template('notification.html', notification="注册成功,3秒后自动跳转登陆界面", web='/')
        else:
            return render_template('register.html', message="填写信息有误！")


@app.route('/notification/')
def notification():
    return "notification"


@login_required
@app.route('/panel/')
def panel():
    users = User.query.order_by(User.id).all()
    return render_template('panel.html', users=users)


@login_required
@app.route('/documents/')
def documents():
    return render_template('documents.html')


@login_required
@app.route('/download/')
def download():
    return send_from_directory('static', 'software/v2rayN-Core.zip')


@login_required
@app.route('/tool/', methods=['GET', 'POST'])
def tool():
    if request.method == 'GET':
        return render_template("tool.html")
    else:
        youtube_url = request.form.get('youtube_url')
        command = "youtube-dl " + youtube_url
        youtube_dl = subprocess.Popen(args=command, shell=True)
        return render_template("tool.html")


# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
