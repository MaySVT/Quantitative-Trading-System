import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gplearn
import talib
from gp_extend_func import *
from gplearn import genetic
import gplearn
from factor import factor
from flask_socketio import SocketIO, emit
from Evaluate import Evaluation

class ga:
    def __init__(self, df,factor_list):
        self.factor_list = factor_list
        self.factors = factor(df)
        self.data = self.get_data()
        self.new_factor_list = []
        self.functions = self.function_set()

    def get_data(self):
        for f in self.factor_list:
            eval("self.factors.get_"+f+"()")
        tmp = self.factors.get_df()
        tmp = tmp.fillna(method = 'bfill').fillna(method = 'ffill')
        tmp['pnl'] = tmp.close/tmp.open-1
        return tmp

    def function_set(self):
        gp_add_ = gplearn.functions.make_function(function=gp_add, name='gp_add', arity=2)
        gp_sub_ = gplearn.functions.make_function(function=gp_sub, name='gp_sub', arity=2)
        gp_mul_ = gplearn.functions.make_function(function=gp_mul, name='gp_mul', arity=2)
        gp_div_ = gplearn.functions.make_function(function=gp_div, name='gp_div', arity=2)
        gp_max_ = gplearn.functions.make_function(function=gp_max, name='gp_max', arity=2)
        gp_min_ = gplearn.functions.make_function(function=gp_min, name='gp_min', arity=2)
        gp_sqrt_ = gplearn.functions.make_function(function=gp_sqrt, name='gp_sqrt', arity=1)
        gp_log_ = gplearn.functions.make_function(function=gp_log, name='gp_log', arity=1)
        gp_neg_ = gplearn.functions.make_function(function=gp_neg, name='gp_neg', arity=1)
        gp_inv_ = gplearn.functions.make_function(function=gp_inv, name='gp_inv', arity=1)
        gp_abs_ = gplearn.functions.make_function(function=gp_abs, name='gp_abs', arity=1)
        gp_sin_ = gplearn.functions.make_function(function=gp_sin, name='gp_sin', arity=1)
        gp_cos_ = gplearn.functions.make_function(function=gp_cos, name='gp_cos', arity=1)
        gp_tan_ = gplearn.functions.make_function(function=gp_tan, name='gp_tan', arity=1)
        gp_sig_ = gplearn.functions.make_function(function=gp_sig, name='gp_sig', arity=1)
        delta_ = gplearn.functions.make_function(function=delta, name='delta', arity=1)
        delay_ = gplearn.functions.make_function(function=delay, name='delay', arity=1)
        sma_ = gplearn.functions.make_function(function=sma, name='sma', arity=1)
        stddev_ = gplearn.functions.make_function(function=stddev, name='stddev', arity=1)
        product_ = gplearn.functions.make_function(function=product, name='product', arity=1)
        ts_min_ = gplearn.functions.make_function(function=ts_min, name='ts_min', arity=1)
        ts_max_ = gplearn.functions.make_function(function=ts_max, name='ts_max', arity=1)
        ts_argmax_ = gplearn.functions.make_function(function=ts_argmax, name='ts_argmax', arity=1)
        ts_argmin_ = gplearn.functions.make_function(function=ts_argmin, name='ts_argmin', arity=1)
        ts_sum_ = gplearn.functions.make_function(function=ts_sum, name='ts_sum', arity=1)

        init_function = [gp_add_, gp_sub_, gp_mul_, gp_div_, 
                        gp_sqrt_, gp_log_, gp_neg_, gp_inv_, 
                        gp_abs_, gp_max_, gp_min_, gp_sin_,
                        gp_cos_, gp_tan_, gp_sig_]
        user_function = [delta_, delay_,sma_, stddev_, product_,ts_min_, ts_max_, ts_argmax_, ts_argmin_,ts_sum_]
        return init_function+user_function
    

    def gp(self, generations = 3,population_size = 20,tournament_size = 10,hall_of_fame = 20,
            n_components = 5,random_state=666,n_jobs = -1,
            init_method ='half and half',init_depth =(2,4)):

        gp_ = genetic.SymbolicTransformer(
                                feature_names= self.factor_list,           #基础行情数据的变量名
                                function_set=self.functions,          #迭代的函数公式
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
        X = self.get_data()[self.factor_list][:-1]
        y = self.get_data()['pnl'][1:]

        # for generation in range(generations):
        #     gp_.generation = generation  # 设置当前代数
        #     gp_.run(X, y)  # 执行遗传算法的一代操作

        #     progress = (generation + 1) / generations * 100
        #     message = f"Generation {generation + 1}/{generations}"

        #     emit('genetic_algorithm_progress', {
        #         'progress': progress,
        #         'message': message
        #     })
        #     socketio.sleep(1)  
        gp_.fit(X,y)

        for g in gp_:
            self.new_factor_list.append(str(g))

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
    
    def feature_imp(self):
        eva = Evaluation(self.data,self.factor_list+self.new_factor_list)
        return eva.get_featureimportance()
    

from gplearn.genetic import SymbolicRegressor

from flask_socketio import emit  # 假设你在Flask中使用SocketIO来进行WebSocket通信

class CustomSymbolicRegressor(SymbolicRegressor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_generations = kwargs.get('generations', 50)

    def run(self):
        for generation in range(self.total_generations):
            self._generation = generation
            super().run()
            
            # 获取当前代数和进度信息
            progress = (generation + 1) / self.total_generations * 100
            message = f"Generation {generation + 1}/{self.total_generations}"
            
            # 将进度信息发送到前端
            emit('genetic_algorithm_progress', {
                'progress': progress,
                'message': message
            })

