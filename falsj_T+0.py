import numpy as np
import pandas as pd
import time

# 导入数据

def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 定义全局变量, 保存要选股出来的股票
    g.stocks = ["159905.XSHE"]
    #分仓数量
    g.buy_stock_count = 1

      # 每分钟运行
    run_daily(exchange, time='every_bar')
    

def exchange(context):
    hour = context.current_dt.hour
    minute = context.current_dt.minute
    position_count = len(context.portfolio.positions)
    #如果持有小于2只股
    if(position_count <= g.buy_stock_count):
        if hour < 15:
            for stock in g.stocks:
                h = attribute_history(stock, 1, '1d', ('close','high','open','low'))
                    #最新价
                current_data = get_current_data()
                last_price =  current_data[stock].last_price
                high_limit =  current_data[stock].high_limit
                day_open = current_data[stock].day_open
                if last_price > h['high'][-1]:# and day_open/stock_close<1.09:
                    adjust_position2(context,stock)
                    break
    #卖出
    
    sell_list = set(context.portfolio.positions.keys())
    for stock in sell_list:
        #当前价格(上一分钟)
        h = attribute_history(stock, 2, '1d', ('close','open','low','high'))
        current_data = get_current_data()
        last_price =  current_data[stock].last_price
        #开盘价往下走5%卖出
        if last_price < h['low'][-1]:# and stock_close1 < high_limit
            #清空卖出
            order_target_value(stock, 0)
         
def adjust_position2(context, stock):
    # 买入的股票
        position_count = len(context.portfolio.positions)
        if g.buy_stock_count > position_count:
            value = context.portfolio.cash / (g.buy_stock_count - position_count)
            if context.portfolio.positions[stock].total_amount == 0:
                order_target_value(stock, value)