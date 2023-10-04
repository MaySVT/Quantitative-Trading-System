from typing import Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import backtrader as bt
from datetime import datetime
from backtrader.feeds import PandasData
from backtrader import num2date

class factor_calc:
    '''
    calculate factors according to strategy
    '''
    def __init__(self,df):
        '''
        input:df:Pandas DataFrame
        '''
        df['trade_time'] = pd.to_datetime(df.trade_time)
        df.index = df['trade_time']
        self.df = df

    def rbreaker(self):
        df = self.df
        high = df.resample('1D')['high'].max()
        low = df.resample('1D')['low'].min()
        close = df.resample('1D')['close'].last()
        pivot = (high+low+close)/3
        price_range = high - low
        p = pivot
        r= price_range

        #calc price_range pivot
        bins = list(r.index[1:])
        bins.append(r.index[-1]+np.timedelta64(1,'D'))
        labels = r.values[1:]
        df['price_range'] = pd.cut(df.index,bins = bins,labels = labels,ordered = False,right = True).astype('float')

        bins = list(p.index[1:])
        bins.append(p.index[-1]+np.timedelta64(1,'D'))
        labels = p.values[1:]
        df['pivot'] = pd.cut(df.index,bins = bins,labels = labels,ordered = False,right = True).astype('float')   
    
    def get_df(self):
        return self.df

class PandasData_rbreaker(PandasData):
    lines = ('pivot','price_range')
    params = (
        ('pivot', 10),
        ('price_range',9)
    )

class data_prepare:
    def __init__(self,df):
        self.df = df
    
    def rbreaker(self):
        feeds = PandasData_rbreaker(
                dataname=self.df,
                datetime=1,  
                open=2, 
                high=4,  
                low=5,  
                close=3,  
                volume=6,  
                openinterest=-1,  
                price_range=9,  
                pivot = 10
            )
        return feeds


class R_breaker(bt.Strategy):
    params=(('k1',0.5),
            ('k2',0.1),
            ('size',1),
           )
    
    
    def __init__(self):
        
        self.pivot = self.datas[0].pivot
        self.price_range = self.datas[0].price_range   
        self.open = self.datas[0].open
        self.order = None
        self.log = []
        self.price = []

    def next(self):
        if self.position.size == 0:
            if self.open[0] > self.pivot[0] + self.params.k2*self.price_range[0]:
                self.order = self.buy(size=self.params.size,tradeid = 1) 
            if self.open[0] < self.pivot[0] + self.params.k1*self.price_range[0]:
                self.order = self.sell(size = self.params.size,tradeid = 0)
        if self.position.size > 0 :
            if self.open[0] > self.pivot[0] - self.params.k2*self.price_range[0]:
                self.order = self.close(tradeid = 1)
                self.order = self.sell(size = self.params.size,tradeid = 0)
        if self.position.size < 0 :
            if self.open[0] < self.pivot[0] - self.params.k1*self.price_range[0]:
                self.order = self.close(tradeid = 0)
                self.order = self.buy(size = self.params.size,tradeid = 1)
                
                
    def notify_trade(self, trade):
        if trade.justopened:
            return self.price.append(trade.price)
        elif trade.isclosed: 
            self.log.append([num2date(trade.dtopen),num2date(trade.dtclose),trade.tradeid,self.price[-1],trade.pnl, trade.pnlcomm])
        else:
            return


class strategy:
    def __init__(self,feeds,startcash1=10000,commission1=0.002,slippage_perc1 = 0.02):
        # initialize cerebro engine
        cerebro = bt.Cerebro()  
        cerebro.adddata(feeds)
        cerebro.broker.setcash(startcash1) 
        cerebro.broker.setcommission(commission = commission1) 
        cerebro.broker.set_slippage_perc(slippage_perc1)
        # add analyzer
        cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.003, annualize=True, _name='SharpeRatio')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
        self.cerebro = cerebro
        self.log = None
        self.annualreturn = None
        self.sharperatio = None
        self.maxdrawdown = None

    def rbreaker(self):
        cerebro = self.cerebro
        cerebro.addstrategy(R_breaker) 
        #run engine
        analyzer_data = cerebro.run()

        #get log
        log = pd.DataFrame(analyzer_data[0].log)
        log.columns = ['starttime','closetime','side','price','pnl','pnlcomm']
        log['starttime'] = pd.to_datetime(log['starttime'])
        #log['side'] = log.side.apply(lambda x: 'BUY' if x == 1 else 'SELL')
        self.log = log

        #get evaluation
        self.annualreturn = dict(analyzer_data[0].analyzers.AnnualReturn.get_analysis())
        #print(analyzer_data[0].analyzers.SharpeRatio.get_analysis())
        self.sharperatio = analyzer_data[0].analyzers.SharpeRatio.get_analysis()['sharperatio']
        self.maxdrawdown = {'最大回撤':analyzer_data[0].analyzers.DrawDown.get_analysis()['max']['drawdown'],
                            '最大资金回撤':analyzer_data[0].analyzers.DrawDown.get_analysis()['max']['moneydown']
                            }
        self.tradeanalyzer = {'盈利交易数':analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['won']['total'],
                              '单笔平均盈利':analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['won']['pnl']['average'],
                              '亏损交易数':analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['lost']['total'],
                              '单笔平均亏损':analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['lost']['pnl']['average'],
                              '胜率':analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['won']['total']/(analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['won']['total'] + analyzer_data[0].analyzers.TradeAnalyzer.get_analysis()['lost']['total'])
        }
