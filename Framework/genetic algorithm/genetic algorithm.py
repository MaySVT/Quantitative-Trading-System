import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gplearn
import talib
from gp_extend_func import *
from gplearn import genetic
import gplearn
from factor import factor

class ga:
    def __init__(self, df,factor_list):
        self.factor_list = factor_list
        self.factors = factor(df)
        self.data = self.get_data()
        self.new_factor_list = []

    def get_data(self):
        for f in self.factor_list:
            eval("self.factors.get_"+f+"()")
        tmp = self.factors.get_df()
        tmp = tmp.fillna(method = 'bfill').fillna(method = 'ffill')
        tmp['pnl'] = tmp.close - tmp.open
        return tmp

    def function_set(self):
        gp_add = gplearn.functions.make_function(function=gp_add, name='gp_add', arity=2)
        gp_sub = gplearn.functions.make_function(function=gp_sub, name='gp_sub', arity=2)
        gp_mul = gplearn.functions.make_function(function=gp_mul, name='gp_mul', arity=2)
        gp_div = gplearn.functions.make_function(function=gp_div, name='gp_div', arity=2)
        gp_max = gplearn.functions.make_function(function=gp_max, name='gp_max', arity=2)
        gp_min = gplearn.functions.make_function(function=gp_min, name='gp_min', arity=2)
        gp_sqrt = gplearn.functions.make_function(function=gp_sqrt, name='gp_sqrt', arity=1)
        gp_log = gplearn.functions.make_function(function=gp_log, name='gp_log', arity=1)
        gp_neg = gplearn.functions.make_function(function=gp_neg, name='gp_neg', arity=1)
        gp_inv = gplearn.functions.make_function(function=gp_inv, name='gp_inv', arity=1)
        gp_abs = gplearn.functions.make_function(function=gp_abs, name='gp_abs', arity=1)
        gp_sin = gplearn.functions.make_function(function=gp_sin, name='gp_sin', arity=1)
        gp_cos = gplearn.functions.make_function(function=gp_cos, name='gp_cos', arity=1)
        gp_tan = gplearn.functions.make_function(function=gp_tan, name='gp_tan', arity=1)
        gp_sig = gplearn.functions.make_function(function=gp_sig, name='gp_sig', arity=1)
        delta = gplearn.functions.make_function(function=delta, name='delta', arity=1)
        delay = gplearn.functions.make_function(function=delay, name='delay', arity=1)
        sma = gplearn.functions.make_function(function=sma, name='sma', arity=1)
        stddev = gplearn.functions.make_function(function=stddev, name='stddev', arity=1)
        product = gplearn.functions.make_function(function=product, name='product', arity=1)
        ts_min = gplearn.functions.make_function(function=ts_min, name='ts_min', arity=1)
        ts_max = gplearn.functions.make_function(function=ts_max, name='ts_max', arity=1)
        ts_argmax = gplearn.functions.make_function(function=ts_argmax, name='ts_argmax', arity=1)
        ts_argmin = gplearn.functions.make_function(function=ts_argmin, name='ts_argmin', arity=1)
        ts_sum = gplearn.functions.make_function(function=ts_sum, name='ts_sum', arity=1)

        init_function = [gp_add, gp_sub, gp_mul, gp_div, 
                        gp_sqrt, gp_log, gp_neg, gp_inv, 
                        gp_abs, gp_max, gp_min, gp_sin,
                        gp_cos, gp_tan, gp_sig]
        user_function = [delta, delay,sma, stddev, product,ts_min, ts_max, ts_argmax, ts_argmin,ts_sum]
        return init_function+user_function
    

    def gp(self,generations = 3,population_size = 20,tournament_size = 10,hall_of_fame = 20,
            n_components = 5,random_state=666,n_jobs = -1,
            init_method ='half and half',init_depth =(2,4)):

        gp_ = genetic.SymbolicTransformer(
                                feature_names= self.factor_list,           #基础行情数据的变量名
                                function_set=self.function_set(),          #迭代的函数公式
                                generations=generations,            #迭代的次数
                                metric='spearman',                  #适应度的评价标准
                                population_size=population_size,    #迭代的和序数
                                tournament_size=tournament_size,                
                                random_state=random_state,
                                hall_of_fame = hall_of_fame,                   
                                n_components = n_components,
                                n_jobs =n_jobs,
                                init_method=init_method,
                                init_depth = init_depth,
                                verbose=1
                                )
        gp_.fit(self.get_data()[self.factor_list][:-1], self.get_data()['pnl'][1:])
        self.new_factor_list = gp_
        return gp_
    
    def generate_new_factor(self):
        for factor in self.factor_list:
            locals()[factor] = self.data[factor].to_numpy()
        for g in self.new_factor_list:
            self.data[str(g)]=eval(str(g))
    
    def IC(self):
        tmp = {}
        for c in self.factor_list+self.new_factor_list:
            tmp[c] = self.data[c][:-1].corr(self.data['pnl'][1:])
        return tmp