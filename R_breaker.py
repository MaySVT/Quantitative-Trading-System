#!/usr/bin/env python
# coding: utf-8

# In[1]:


from jqdatasdk import *
import pandas as pd
import time
import datetime
import math


# In[2]:


auth("17701835191",'18901869188Lrd')


# In[3]:


df_AG=get_price('AP2304.XZCE', start_date='2022-04-19', end_date='2022-10-19',frequency = '1m')


# In[4]:


#获取了半年的一分钟数据
df_AP = df_AG


# In[5]:


df_AP.to_csv('D:\科研1\AP2304.XZCE.csv')


# In[6]:


df_AP


# In[7]:


df_AP


# In[70]:


df_AP['high'].plot()


# R-Breaker策略
# 
# 
# 1）计算6个目标价位
# 
# 
# 观察卖出价（Ssetup）= High + a * (Close – Low)
# 
# 
# 观察买入（Bsetup）= Low – a * (High – Close)
# 
# 
# 反转卖出价（Senter）= b / 2 * (High + Low) – c * Low
# 
# 
# 反转买入价（Benter）= b / 2 * (High + Low) – c * High
# 
# 
# 突破卖出价（Sbreak）= Ssetup - d * (Ssetup – Bsetup)
# 
# 
# 突破买入价（Bbreak）= Bsetup + d * (Ssetup – Bsetup)
# 
# 2)策略情况
# 
# 
# 趋势策略情况：
# 
# 
# 若价格>突破买入价，开仓做多
# 
# 
# 若价格<突破卖出价，开仓做空
# 
# 
# 反转策略情况：
# 
# 
# 若日最高价>观察卖出价，然后下跌导致价格<反转卖出价，开仓做空或者反手（先平仓再反向开仓）做空
# 
# 
# 若日最低价<观察买入价，然后上涨导致价格>反转买入价，开仓做多或者反手（先平仓再反向开仓）做多
# 
# 若当前x分钟的最高价>观察卖出价，认为它已经到了当日阻力位，可能发生行情反转，在反转卖出价挂上卖出开仓的停止单
# 
# 
# 若当前x分钟的最低价<观察买入价，认为它已经到了当日支撑位，可能发生行情反转，在反转买入价挂上买入开仓的停止单

# ![figure1](https://pic4.zhimg.com/v2-1fb619fdadf8faddea6292a56778206f_r.jpg)

# In[71]:


def write_log(situation,data_deal,i):
    if situation == 0:
        print("时间：{},止损平仓".format(data_deal.index[i]))
    if situation == 1:
        print("时间：{},空仓条件下价格超过突破买入价,开多仓".format(data_deal.index[i]))
    if situation == 2:
        print("时间：{},空仓条件下价格跌破突破卖出价,开空仓".format(data_deal.index[i]))
    if situation == 3:
        print("时间：{},持多仓时日内最高价超过观察卖出价且跌破反转卖出价,先平仓后做空".format(data_deal.index[i]))
    if situation == 4:
        print("时间：{},持空仓时日内最低价跌破观察买入价且突破反转买入价,先平仓后做多".format(data_deal.index[i]))
    return


# In[72]:


def R_Breaker(data,loss_price,initial_cash,service_charge,max_lot):
    #data:由于我数据访问到上限了，所以直接使用dataframe,实际上可以只给security，start_date和end_date,然后获取data
    #loss_price:止损比例
    #initial_cash:投入
    #service_charge:手续费/手
    #deposit_rate:保证金比率/手
    #max_lot:最大交易手数
    #初始化总资产、活动金额、保证金金额、手数(做空为负，做多为正）、当前天数、结果表
    total_cash = initial_cash
    cash_account = initial_cash
    deposit_cash = 0
    total_lot = 0
    #n1:data;n2:result
    n1 = 0
    n2 = 0
    df_result = pd.DataFrame(columns = ['date','high','low','close','deal','cash_account','total_lot','total_cash'])
    if n2==0:
        high = data[data.index < data.index[n1]+datetime.timedelta(days= 1)]['high'].max()
        low =  data[data.index < data.index[n1]+datetime.timedelta(days= 1)]['high'].min()
        close = data[data.index<data.index[n1]+datetime.timedelta(days= 1)].iloc[-1]['close']
        df_result.loc[n2] = [datetime.datetime.strftime(data.index[n1],"%Y-%m-%d"),high,low,close,0,cash_account,total_lot,total_cash]
        n1 = len(data[data.index<data.index[n1]+datetime.timedelta(days= 1)])
        n2 = n2 + 1
    if n2 != 0:
        while n1<len(data):
            deal = 0
            high = df_result.iloc[n2-1]['high']
            low = df_result.iloc[n2-1]['low']
            close = df_result.iloc[n2-1]['close']
            pivot = (high + low + close) / 3  # 枢轴点
            breakbuy = high + 2 * (pivot - low) # 突破买入价
            setupsell = pivot + (high - low) # 观察卖出价
            revsell = 2 * pivot - low# 反转卖出价
            revbuy =  2 * pivot - high # 反转买入价
            setupbuy = pivot - (high - low), # 观察买入价
            breaksell = low - 2 * (high - pivot)  # 突破卖出价
            #position:多仓：1，空仓：0
            #超过观察卖出价:是1否0
            setupsell_index = 0
            #跌破观察买入价：是1否0
            setupbuy_index = 0
            #日内数据
            data_deal = data[(data.index<data.index[n1]+datetime.timedelta(days= 1))&(data.index>=data.index[n1])]
            #获得日内最高价、最低价、收盘价
            high = data_deal['high'].max()
            low = data_deal['low'].min()
            close = data_deal.iloc[-1]['close']
            for i in range(0,len(data_deal)):
                #检查是否超过观察卖出价或者跌破观察买入价
                if data_deal.iloc[i]['high'] > setupsell:
                    setupsell_index = 1
                if data_deal.iloc[i]['high'] < setupbuy:
                    setupbuy_index = 1
                #检查止损
                #当前总资产
                total_cash = cash_account + total_lot*data_deal.iloc[i]['high']
                loss = (initial_cash - total_cash)/initial_cash*100
                #超过止损点,平仓
                if loss > loss_price:
                    cash_account = cash_account + total_lot * data_deal.iloc[i]['high'] - abs(total_lot)*service_charge
                    deal += abs(total_lot)
                    total_lot = 0
                    write_log(0,data_deal,i)
                 #未超过止损点
                else:
                    #空仓时
                    if total_lot == 0:
                        #价格超过突破买入价
                        if data_deal.iloc[i]['high']>breakbuy:
                            #做多
                            total_lot += max_lot
                            deal += max_lot
                            cash_account -= max_lot * (data_deal.iloc[i]['high'] + service_charge)
                            position = 1
                            write_log(1,data_deal,i)
                        #价格低过突破卖出价
                        if (data_deal.iloc[i]['high']<breaksell):
                            #做空
                            total_lot -= max_lot
                            deal += max_lot
                            cash_account += max_lot * (data_deal.iloc[i]['high'] - service_charge)
                            position = 0 
                            write_log(2,data_deal,i)
                    #持仓时
                    else:
                        #如果做多仓
                        if position:
                            #如果日内价格已超过观察卖出价
                            if setupsell_index:
                                #如果跌破反转卖出价,则先平仓再做空
                                if data_deal.iloc[i]['high'] < revsell:
                                    #平仓
                                    cash_account += total_lot*(data_deal.iloc[i]['high']-service_charge)
                                    deal += abs(total_lot)
                                    total_lot = 0
                                    #做空
                                    position = 0
                                    total_lot -= max_lot
                                    deal += abs(total_lot)
                                    cash_account += max_lot * (data_deal.iloc[i]['high'] - service_charge)
                                    write_log(3,data_deal,i)
                        #如果做空仓
                        else:
                            #如果日内最低价已跌破观察买入价
                            if setupbuy_index:
                            #如果突破反转买入价，先平仓再做多
                                if data_deal.iloc[i]['high'] > revbuy:
                                    #平仓
                                    cash_account -= abs(total_lot)*(data_deal.iloc[i]['high']+service_charge)
                                    deal += abs(total_lot)
                                    total_lot = 0
                                    #做多
                                    position = 1
                                    total_lot += max_lot
                                    deal += max_lot
                                    cash_account -= max_lot * (data_deal.iloc[i]['high']+service_charge)
                                    write_log(4,data_deal,i)
            total_cash = cash_account + total_lot*close   
            df_result.loc[n2] = [datetime.datetime.strftime(data.index[n1],"%Y-%m-%d"),high,low,close,deal,cash_account,total_lot,total_cash]  
            n2 += 1
            n1 = n1 + len(data_deal)
        return df_result
        
        


# In[90]:


df2 = R_Breaker(df_AP,50,50000,15,2)


# In[92]:


df_AP['2022-09-30':'2022-09-30']['high'].plot()


# In[94]:


df2['total_cash'].plot()


# 所以说趋势跟踪策略在震荡行情下只会大赔特赔啊！！！投资需谨慎，理财有风险！！
