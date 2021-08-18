# flask 小型博客

## 项目构架

* nginx 作为web服务器

* gunicorn 提供 WSGI HTTP 服务

* flask 作为后端

* mariadb 作为数据库

## 环境

debian 9 

python 3.7 （亲测依赖模块不适用于2.7与3.8）

## 部署

1. 下载所需要的组件

```sh
apt install nginx

apt install mariadb-server 

#apt install mariadb-client

apt install python3

apt install python3-pip

pip3 install gunicorn

pip3 install supervisor

apt install git

cd 到你想存放网站数据的地方

git clone 本项目

```

2. 修改nginx配置文件

在 http{ } 中增加该server块，用于将80代理到gunicorn的8000端口

```
  server {
    listen 80;
    server_name example.org;
    access_log  /var/log/nginx/example.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
```

如果nginx已经启动，则重载配置文件

nginx -s reload

3. 使用supervisor监控gunicorn的运行

如果是第一次使用supervisor，请参考http://supervisord.org/

3.1 生成supervisor的配置文件 

```
sudo echo_supervisord_conf > /etc/supervisord.conf
```

3.2 修改配置文件，在其中加入

```
[program:gunicorn]
command=gunicorn app:app
directory=/path/to/project # 此处改为项目地址，也就是flask_web目录
user=nobody
autostart=true
autorestart=true
redirect_stderr=true
```

这是在监控目录中加入程序：gunicorn

3.3 启动supervisor

supervisord -c /etc/supervisord.conf 

3.4 supervisor理解

supervisor分为两部分

supervisord是一个服务端，监听于9001端口

supervisorctl是一个客户端，用于控制与查看server的状态

4. 数据库的部署与启动

mysql的rpm安装比较容易出错，所以建议采用apt install mariadb的方式安装

它的原理也和supervisor类似，一个server，一个client。

mysqld 启动服务端，配置好账号密码，如果要远程控制数据库的话要，**开启远程访问**，不然只能本地使用数据库。

4.1 创建数据库flask

4.2 修改config.py文件中的

```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@ip:3306/flask'
```

5. 数据库迁移同步

用于完成ORM映射

```sh
cd 项目目录

python3 manage db init

python3 manage db upgrade

python3 manage db migrate
```

5. 项目部署完毕！