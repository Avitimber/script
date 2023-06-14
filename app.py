#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Kehang Tseng time: 2023/6/14
from flask import Flask, render_template, request, redirect, url_for, make_response, json, jsonify, abort
from wtforms import StringField, PasswordField, SubmitField # 类型
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo # 验证数据是否为空 验证数据是否相同
from handler import Login, AdminSignin, AdminLogin, BuyerSignup, BuyerLogin, SellerSignin, SellerLogin
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'jogqhohgohaohga'

@app.route('/')
def enter():
    return redirect(url_for('welcome'))

@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    form = Login()
    if request.method == 'GET':
        return render_template('welcome.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            passwd = form.passwd.data
            character = request.form.get('character')
            print(type(name), type(passwd), type(character))
            print(name)
            print(passwd)
            print(character)
            if character == '管理员':
                # TODO: 查询数据库是否存在
                pass
            elif character == '买家':
                if True:
                    return redirect(url_for('buyer_signup'))
                pass
            elif character == '卖家':
                pass

            return render_template('demo.html')
        else:
            return render_template('<h1>注册信息有误！</h1>')

@app.route('/buyer_signup', methods = ['GET', 'POST'])
def buyer_signup():
    form = BuyerSignup()
    if request.method == 'GET':
        return render_template('buyer_signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            buyer_name = form.buyer_name.data
            passwd = form.passwd.data
            real_name = form.real_name.data
            id_number = form.id_number.data
            addr = form.addr.data
            print(buyer_name, passwd, real_name, id_number, addr)
            #TODO: 数据插入 buyer
            return redirect(url_for('buyer_home'))
        else:
            return render_template('signin_error.html')

@app.route('/buyer_home')
def buyer_home():
    data = [
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
        ['数据1', '数据2', '数据3', '数据4', '数据5', '数据6'],
    ]
    json_data = json.dumps(data)

    return render_template('demo2.html', detail = json_data)

if __name__ == '__main__':
    app.run(debug = True)
