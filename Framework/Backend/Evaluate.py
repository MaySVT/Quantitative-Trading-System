import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from math import sqrt
import warnings
warnings.filterwarnings("ignore")
def drop_extreme_value(df,factor,k):
    '''
    输入：因子名称，修正std范围k
    输出：盖帽后的因子值
    '''
    tmp = df[factor]
    mean = tmp.mean()
    std = tmp.std()
    return tmp.clip(lower =mean-k*std,upper = mean+k*std)

class Evaluation():
    def __init__(self,df,factor_lst):
        '''
        input:含有open_time high low close volume pct 和 Factor,index 为 时间的DataFrame,
        '''
        self.df = df
        #所有因子名称构成的列表
        self.factor_lst = factor_lst # list(df.drop(columns = ['open_time','open','high','low','close','volume','pnl']).columns)
        self.pct = df['pnl']
        #list:按IC IR feature_importance 的因子排序（由高到低）
        self.ic_rank = None
        self.ir_rank = None
        self.feature_importance_rank = None
        #选择出来的新因子
        self.new_factor_lst = None

    def process_extreme(self,k):
        '''
        input:极端值阈值k(偏离均值k个标准差）
        output：处理后的self.df
        '''
        for factor in self.factor_lst:
            self.df[factor] = drop_extreme_value(self.df, factor, k)

    def get_IC(self):
        '''
        input:self
        output:两个列表，第一个是factor_name,第二个是对应IC，均从大至小排列
        '''
        IC_lst = []
        for factor in self.factor_lst:
            IC = (self.pct).corr(self.df[factor])
            IC_lst.append(IC)
        tmp = pd.DataFrame()
        tmp['factor'] = self.factor_lst
        tmp['IC'] = IC_lst
        tmp = tmp.sort_values('IC', ascending=False)
        self.ic_rank = list(tmp.factor)
        return list(tmp.factor), list(tmp.IC)

    def get_rolling_IC(self,factor,t):
        '''
        输入：t为rolling的时间(单位：天）,因子名称
        输出：rolling段的截至时间(是时间戳）和rolling段的IC值(都是list)
        '''
        # delta = self.df.index[1] - self.df.index[0]
        # self.df.resample(on='open_time')
        delta = self.df['open_time'][1]-self.df['open_time'][0]
        k = int(np.timedelta64(t, 'D') / delta)
        ic_lst = []
        for i in range(k - 1, len(self.df)):
            tmp = {}
            tmp1 = self.df.iloc[i - k + 1:i + 1, :][factor]
            tmp2 = self.df.iloc[i - k + 1:i + 1, :]['pnl']
            tmp['time'] = self.df['open_time'][i]
            tmp['rolling_IC'] = tmp1.corr(tmp2)
            ic_lst.append(tmp)
            # resample成天，close.last/open.first
        return ic_lst

    def get_IR(self,t):
        '''
        输入：t为周期时间(单位：天）
        输出：两个列表，第一个是factor_name,第二个是对应IR，均从大至小排列
        '''
        IR_lst = []
        for factor in self.factor_lst:
            tmp = (self.df[factor] * self.df['return']).resample(f'{t}D').sum() / ((self.df[factor] * self.df[factor]).resample(f'{t}D').sum().apply(lambda x: sqrt(x))) * ((self.df['return'] * self.df['return']).resample(f'{t}D').sum().apply(lambda x: sqrt(x)))
            ir = tmp.mean() / tmp.std() * np.sqrt(len(tmp))
            IR_lst.append(ir)
        tmp = pd.DataFrame()
        tmp['factor'] = self.factor_lst
        tmp['IR'] = IR_lst
        tmp = tmp.sort_values('IC', ascending=False)
        self.ir_rank = list(tmp.factor)
        return list(tmp.factor), list(tmp.IR)

    def get_featureimportance(self):
        X = self.df[self.factor_lst]
        y = self.pct
        Xtrain,Xval,ytrain,yval = train_test_split(X, y, test_size=0.8)
        reg_mod = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.08,
            subsample=0.75,
            colsample_bytree=1,
            max_depth=6,
            gamma=0,
        )
        eval_set = [(Xtrain, ytrain), (Xval, yval)]
        reg_mod.fit(Xtrain, ytrain, eval_set=eval_set, eval_metric='rmse', verbose=False)
        factor = list(reg_mod.feature_names_in_)
        importance = list(reg_mod.feature_importances_)
        tmp = pd.DataFrame()
        tmp['factor'] = factor
        tmp['importance'] = importance
        tmp = tmp.sort_values('importance', ascending=False)
        self.feature_importance_rank = list(tmp.factor)
        return tmp # list(tmp.factor), list(tmp.importance)

    def get_new_factor_lst(self,r1,r2,r3):
        '''
        :param r1: 选择ic前r1名
        :param r2: 选择ir前r2名
        :param r3: 选择fi前r3名
        :return:选择出来的因子名称构成的list
        '''
        ic_lst = self.ic_rank
        ir_lst = self.ir_rank
        fi_lst = self.feature_importance_rank
        if len(ic_lst) > r1:
            new_ic_lst = ic_lst[:r1]
        else:
            new_ic_lst = ic_lst
        if len(ir_lst) > r2:
            new_ir_lst = ir_lst[:r2]
        else:
            new_ir_lst = ir_lst
        if len(fi_lst) > r1:
            new_fi_lst = fi_lst[:r3]
        else:
            new_fi_lst = fi_lst
        tmp = new_ic_lst.extend(new_ir_lst)
        tmp = new_fi_lst.extend(tmp)
        lst = list(set(tmp))
        self.new_factor_lst = lst
        return lst