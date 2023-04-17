from flask import Flask, render_template,request
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import string
# from sqlalchemy import ForeignKey, create_engine
# from sqlalchemy.engine import URL
# import psycopg2
import requests
import string
import math
import json
# import simplejson
import datetime
import copy
import random
import pandas as pd
import numpy as np
import csv
# import oss2
import pandas as pd
from datetime import date, timedelta
import tushare as ts
from werkzeug.utils import secure_filename
import sys
import os


sys.path.append(r'.\system strategy')
from R_breaker import R_breaker

app = Flask(__name__)
CORS(app)

# 注释处代码为需要连接自建数据库时使用
'''class c_overview(db.Model):
    __tablename__ = 'c_overview'
    days = db.Column('f_days',db.Integer,primary_key = True)
    blocks = db.Column('f_blocks',db.Integer)
    deposits = db.Column('f_justification_delay',db.Integer)'''

token='bdb08afc499e166575426cccc5aae85ae04cdb4196cd512ef310d04e'
ts.set_token(token)
pro = ts.pro_api()
index = 1

def time_tran(time):
        '''
        把Ymd转化为Y-m-d，方便后续处理
        '''
        year = time[0:4]
        month = time[4:6]
        date = time[6:]
        date_str = year + '-' + month + '-' + date
        return date_str

def is_time(time):
    is_index = 0
    if len(time) == 8:
        date_str = time_tran(time)
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            pass
        else:
            is_index = 1
    return is_index

# 函数用处为读取本地样本函数，方便展示
# 若直连API，需要类似爬虫的requests函数、方法
def trade(begin, end):
    with open(r"D:\UPenn大三下\Denghui Project\Quantitative-Trading-System\Framework\Backend\TRADE_processed.csv") as f:
        row = csv.reader(f,delimiter = ',')
        next(row)
        r = next(row)
        while eval(r[3]) < begin:
            r = next(row)
        trd = []
        while eval(r[3]) <= end:
            t = {}
            t['id'] = eval(r[0])
            t['price'] = eval(r[1])
            t['vol'] = eval(r[2])
            t['time'] = eval(r[3])
            trd.append(t)
            r = next(row)
    return trd

def sample(asset):
    data = pd.DataFrame(columns=['hour','high','low','PDC','current'])
    data['hour'] = pd.read_csv(r'.\..\Data\pre_cp_adj_fake.csv')['hour']
    data['PDC'] = pd.read_csv(r'.\..\Data\pre_cp_adj_fake.csv')[asset]
    data['high'] = pd.read_csv(r'.\..\Data\high_adj_fake.csv')[asset]
    data['low'] = pd.read_csv(r'.\..\Data\low_adj_fake.csv')[asset]
    data['current'] = pd.read_csv(r'.\..\Data\cp_adj_fake.csv')[asset]
    s = []
    for i in range(len(data)):
        t = {}
        t['hour'] = data['hour'][i]
        t['PDC'] = data['PDC'][i].item()
        t['high'] = data['high'][i].item()
        t['low'] = data['low'][i].item()
        t['current'] = data['current'][i].item()
        s.append(t)
    return s

def sample1(asset):
    data = []
    id = 0
    with open(r'.\..\Data\pre_cp_adj_fake.csv') as f:
        row = csv.reader(f,delimiter = ',')
        r = next(row)
        id = r.index(asset)
        for r in row:
            t = {}
            t['hour'] = r[0]
            if r[id]=="":
                t['PDC'] = 0
            else:
                t['PDC'] = eval(r[id])
            data.append(t)

    with open(r'.\..\Data\high_adj_fake.csv') as f:
        row = csv.reader(f,delimiter = ',')
        r = next(row)
        id = r.index(asset)
        for i in range(len(data)):
            r = next(row)
            data[i]['high'] = eval(r[id])

    with open(r'.\..\Data\low_adj_fake.csv') as f:
        row = csv.reader(f,delimiter = ',')
        r = next(row)
        id = r.index(asset)
        for i in range(len(data)):
            r = next(row)
            data[i]['low'] = eval(r[id])

    with open(r'.\..\Data\cp_adj_fake.csv') as f:
        row = csv.reader(f,delimiter = ',')
        r = next(row)
        id = r.index(asset)
        for i in range(len(data)):
            r = next(row)
            data[i]['current'] = eval(r[id])
    return data

# flask创建页面链接
# 例子中若输入网页http://127.0.0.1:5000/Trade/?beg=1645315199996&end=1645315200005
# http://127.0.0.1:5000/Trade/?beg=开始时间串&end=结束时间串，应该可以出现样本csv中一系列数据
@app.route('/Trade/',methods = ['GET'])
def Trade():
    begin = eval(request.args.get('beg'))
    end = eval(request.args.get('end'))
    trd = trade(begin,end)
    return json.dumps(trd)

@app.route('/Sample/<string:asset>',methods = ['GET'])
def Sample(asset):
    data = sample1(asset)
    return json.dumps(data)

@app.route('/',methods=['GET'])
def index():
    return "Hello Vue"

ALLOWED_EXTENSIONS = ['py']
UPLOAD_FOLDER = '.\\upload'
ALLOWED_STRATEGY = ['R_breaker','Dual_Thrust','ATR']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/<ts_code>/st=<start_time>ed=<end_time>freq=<frequency>/strategy=<stg>',methods=['POST', 'GET'])
def goal_4(ts_code,start_time,end_time,frequency,stg):
    '''
    查询strategy是否正确：目前先假设只有custum
    获取策略
    返回仓位
    '''
    if stg not in ALLOWED_STRATEGY and stg!='custom':
        return  "系统暂不支持该策略，请查询使用指南"
    else:
        #如果策略为CUSTOM：返回HTML页面供用户返回POST请求
        if stg == 'custom':
            if request.method == 'GET':
                return render_template('upload.html')
            if request.method == 'POST':
                file = request.files['file']
                #
                if file and allowed_file(file.filename):
                    global index
                    filename1 = 'strategy'+str(index)+'.py'
                    filename2 = 'strategy'+str(index)
                    strategyname = 'my_strategy'+str(index)
                    index += 1
                    #保存文件至本地
                    file.save(os.path.join(UPLOAD_FOLDER,filename1))
                    #获取函数
                    sys.path.append(r'.\upload')
                    md = __import__(filename2)
                    #获得数据
                    #data = get_data(ts_code,start_time,end_time,frequency)
                    #此处为了避免限制，先使用后台数据，后面注释掉就好
                    data = pd.read_csv(r'.\data.csv')
                    data['trade_time'] = data['trade_time'].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
                    #升序排列
                    data.sort_values(by = 'trade_time',ascending = True,inplace = True,ignore_index = True)
                    #运行自定义策略，得到结果
                    result = md.my_strategy(data)
                    return result.to_json(orient="records", force_ascii=False)
                else:
                    return '文件后缀名必须为.py'
        else:
            if stg == 'R_breaker':
                #获得数据
                #data = get_data(ts_code,start_time,end_time,frequency)
                #此处为了避免限制，先使用后台数据，后面注释掉就好
                data = pd.read_csv(r'Framework\Backend\data.csv')
                data['trade_time'] = data['trade_time'].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
                #升序排列
                data.sort_values(by = 'trade_time',ascending = True,inplace = True,ignore_index = True)
                #运行自定义策略，得到结果
                result = R_breaker(data)
                return result.to_json(orient="records", force_ascii=False)
        
if __name__ == '__main__':
    app.run(debug=True)