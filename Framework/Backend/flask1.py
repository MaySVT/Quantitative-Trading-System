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

app = Flask(__name__)
CORS(app)

# 注释处代码为需要连接自建数据库时使用
'''class c_overview(db.Model):
    __tablename__ = 'c_overview'
    days = db.Column('f_days',db.Integer,primary_key = True)
    blocks = db.Column('f_blocks',db.Integer)
    deposits = db.Column('f_justification_delay',db.Integer)'''

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


if __name__ == '__main__':
    app.run(debug=True)