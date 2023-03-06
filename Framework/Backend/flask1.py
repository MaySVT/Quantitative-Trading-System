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
    with open(r"D:\UPenn大三下\Denghui Project\Quantitative-Trading-System\System Framework\Backend\TRADE_processed.csv") as f:
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


# flask创建页面链接
# 例子中若输入网页http://127.0.0.1:5000/Trade/?beg=1645315199996&end=1645315200005
# http://127.0.0.1:5000/Trade/?beg=开始时间串&end=结束时间串，应该可以出现样本csv中一系列数据
@app.route('/Trade/',methods = ['GET'])
def Trade():
    begin = eval(request.args.get('beg'))
    end = eval(request.args.get('end'))
    trd = trade(begin,end)
    return json.dumps(trd)

@app.route('/',methods=['GET'])
def index():
    return "Hello Vue"


if __name__ == '__main__':
    app.run(debug=True)