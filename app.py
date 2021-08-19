# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session

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
        message = "欢迎~"
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
            return redirect('/')


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
    return "进入注册页面"


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
