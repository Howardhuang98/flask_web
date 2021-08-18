#encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@huanghao.space:3306/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = True


