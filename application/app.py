#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   app.py
@Contact :   huanghoward@foxmail.com
@Modify Time :    2021/8/10 17:39  
------------      
"""
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()