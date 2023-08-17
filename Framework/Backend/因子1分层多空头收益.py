import pandas as pd
import numpy as np
import math

# 读取股票数据并指定收盘价为数值类型
stock_data = pd.read_csv(r"C:\Users\HanweN\Desktop\WIND_ASHAREEODPRICES.csv")

# 读取中证全指数据并指定开盘价和收盘价为数值类型
benchmark_data = pd.read_csv(r"C:\Users\HanweN\Desktop\WIND_AINDEXEODPRICES.csv")


# 将日期列转换为日期时间类型，并修改为"20131227"格式
stock_data["TRADE_DT_VIRTUAL"] = pd.to_datetime(stock_data["TRADE_DT_VIRTUAL"]).dt.strftime("%Y%m%d")
benchmark_data.rename(columns={"TRADE_DT": "TRADE_DT_VIRTUAL"}, inplace=True)
                               
# 根据股票代码和日期对数据进行排序
stock_data.sort_values(by=["S_INFO_WINDCODE", "TRADE_DT_VIRTUAL"], inplace=True)
benchmark_data.sort_values(by=["TRADE_DT_VIRTUAL"], inplace=True)

# 计算每支股票每日最高价和最低价的比例 t
stock_data["t"] = stock_data["S_DQ_HIGH"] / stock_data["S_DQ_LOW"]

# 计算 t 的标准差，窗口大小为3个月的交易日数量
window_size = 3 * 21  # 三个月的交易日数量
stock_data["Std_t"] = stock_data.groupby("S_INFO_WINDCODE")["t"].rolling(window=window_size, min_periods=1).std().reset_index(0, drop=True)

# 按 t 的标准差进行分层
stock_data["Layer"] = pd.qcut(stock_data["Std_t"], 5, labels=False)

# 获取每支股票每日的收益率
stock_data["Return"] = (stock_data["S_DQ_CLOSE"] - stock_data["S_DQ_OPEN"]) / stock_data["S_DQ_OPEN"]

# 将每支股票的收益率向上移动一行，代表第二天的收益率
stock_data["Next_Day_Return"] = stock_data.groupby("S_INFO_WINDCODE")["Return"].shift(-1)

# 使用pivot_table计算每层每日的平均收益率
layer_returns = stock_data.pivot_table(index="TRADE_DT_VIRTUAL", columns="Layer", values="Next_Day_Return", aggfunc="mean")



### 多头策略
# 获取第五层的数据
layer_5_data = stock_data[stock_data["Layer"] == 4]

# 获取每支股票每日的收益率
layer_5_data["Return"] = (layer_5_data["S_DQ_CLOSE"] - layer_5_data["S_DQ_OPEN"]) / layer_5_data["S_DQ_OPEN"]


# 将每支股票的收益率向上移动一行，代表第二天的收益率
layer_5_data["Next_Day_Return"] = layer_5_data.groupby("S_INFO_WINDCODE")["Return"].shift(-1)
layer_5_data["Next_Day_Return"] = layer_5_data["Next_Day_Return"].dropna()

# 使用pivot_table计算每层每日的平均收益率，并将日期列加入结果
layer_returns1 = layer_5_data.pivot_table(index="TRADE_DT_VIRTUAL", columns="Layer", values="Next_Day_Return", aggfunc="mean")
layer_returns1.reset_index(inplace=True)  # 将日期列重置为数据列
# 重命名layer=4.0这一列为"Layer_4.0"
layer_returns1.rename(columns={4.0: "Layer_5"}, inplace=True)

# 将收益率转换为累积收益率
cumulative_returns1 = (layer_returns1.iloc[:, 1:] + 1).cumprod()  # 从第二列开始计算累积收益率，因为第一列是日期
cumulative_returns1 = cumulative_returns1.dropna()  # 去除缺失值

# 计算累积收益率对应的时间
layer_returns1_new = layer_returns1.copy()
layer_returns1_new ["TRADE_DT_VIRTUAL"] = pd.to_datetime(layer_returns1_new ["TRADE_DT_VIRTUAL"])
total_days = (layer_returns1_new ["TRADE_DT_VIRTUAL"].iloc[-1] - layer_returns1_new ["TRADE_DT_VIRTUAL"].iloc[0]).days + 1



##计算多头策略的收益
# 得到总共累积收益率
total_return1 = cumulative_returns1.iloc[-1] 
# 计算年化收益率
annual_return_continuous_compounding = np.log(1 + total_return1) / (total_days / 252)
annual_return_continuous_compounding_pct = (annual_return_continuous_compounding * 100).round(2)
print("多头策略收益率：", annual_return_continuous_compounding_pct[0], "%")

## 计算最大回撤率
rolling_max1 = layer_returns1["Layer_5"].cummax()
drawdown1 =(rolling_max1-layer_returns1["Layer_5"])/ rolling_max1  -  1
max_drawdown1 = drawdown1.max()
max_drawdown_pct = (max_drawdown1.max() * 100).round(2)  # 计算最大回撤率的百分比
print("最大回撤率：", max_drawdown_pct, "%")

## 计算超额收益率
# 计算中证全指每日收益率
benchmark_data["Benchmark_Return"] = (benchmark_data["S_DQ_CLOSE"] - benchmark_data["S_DQ_CLOSE"].shift(1)) / benchmark_data["S_DQ_CLOSE"].shift(1)

# 合并 layer_returns 和 benchmark_data 根据 TRADE_DT_VIRTUAL
benchmark_data["TRADE_DT_VIRTUAL"]=benchmark_data["TRADE_DT_VIRTUAL"].astype(str)
merged_data1 = pd.merge(layer_returns1, benchmark_data, on="TRADE_DT_VIRTUAL")

# 计算每层的超额收益率
layer_excess_returns1 = merged_data1['Layer_5'] - merged_data1['Benchmark_Return']

# 计算超额收益率，并进行累乘得到累积超额收益率
cumulative_excess_returns1 = (1 + layer_excess_returns1).cumprod()

# 得到总共超额收益率
chaoer_return1 = cumulative_excess_returns1.iloc[-1]

## 计算年化超额收益率
annual_chaoerreturn_continuous_compounding1 = np.log(1 + chaoer_return1 ) / (total_days / 252)
annual_chaoerreturn_continuous_compounding_pct1 = (annual_chaoerreturn_continuous_compounding1 * 100)
print("超额收益率：", annual_chaoerreturn_continuous_compounding_pct1, "%")

## 计算超额收益率的标准差
chaoer_std1 = layer_excess_returns1.std()
chaoer_std1y = chaoer_std1 /math.sqrt(total_days / 252)
chaoer_std_pct1= (chaoer_std1y * 100).round(2) 
print("超额收益率标准差：", chaoer_std_pct1, "%")

## 计算夏普比率
sharp_ratio1 = annual_chaoerreturn_continuous_compounding_pct1 / chaoer_std_pct1
print("夏普比率:", sharp_ratio1)







### 多空策略
# 获取第一层的数据
layer_1_data = stock_data[stock_data["Layer"] == 0]

# 获取每支股票每日的收益率
layer_1_data["Return"] = (layer_1_data["S_DQ_CLOSE"] - layer_1_data["S_DQ_OPEN"]) / layer_1_data["S_DQ_OPEN"]
layer_1_data["Return"].dropna()
# 使用pivot_table计算每层每日的平均收益率，并将日期列加入结果
layer_returns2 = layer_1_data.pivot_table(index="TRADE_DT_VIRTUAL", columns="Layer", values="Return", aggfunc="mean")
layer_returns2.reset_index(inplace=True)  # 将日期列重置为数据列
# 重命名layer=0.0这一列为"Layer_1"
layer_returns2.rename(columns={0.0: "Layer_1"}, inplace=True)

# 合并第一层和第五层每日收益率
benchmark_data["TRADE_DT_VIRTUAL"]=benchmark_data["TRADE_DT_VIRTUAL"].astype(str)
layer_duokong = pd.merge(layer_returns1,layer_returns2,on="TRADE_DT_VIRTUAL")

# 计算多空收益，买第5层，卖第1层
layer_duokong['Return'] = layer_duokong['Layer_5'] - layer_duokong['Layer_1']

# 将收益率转换为累积收益率
cumulative_returns2 = (layer_duokong['Return'] + 1).cumprod()  

# 计算多空策略的收益
total_return2 = cumulative_returns2.iloc[-1] 

# 计算年化收益率
annual_return_continuous_compounding2 = np.log(1 + total_return2) / (total_days / 252)
annual_return_continuous_compounding_pct2 = (annual_return_continuous_compounding2 * 100).round(2)
print("多空策略收益率：", annual_return_continuous_compounding_pct2, "%")

## 计算最大回撤率
rolling_max2 = layer_duokong['Return'].cummax()
drawdown2 =( rolling_max2 - layer_duokong['Return'])/rolling_max2   - 1
max_drawdown2 = drawdown2.max()
max_drawdown_pct2 = (max_drawdown2 * 100).round(2)  # 计算最大回撤率的百分比
print("最大回撤率：", max_drawdown_pct2, "%")

## 计算超额收益率

# 合并 layer_returns 和 benchmark_data 根据 TRADE_DT_VIRTUAL
merged_data2 = pd.merge(layer_duokong, benchmark_data, on="TRADE_DT_VIRTUAL")

# 计算每层的超额收益率
layer_excess_returns2 = merged_data2['Return'] - merged_data2['Benchmark_Return']

# 计算超额收益率，并进行累乘得到累积超额收益率
cumulative_excess_returns2 = (1 + layer_excess_returns2).cumprod()

# 得到总共超额收益率
chaoer_return2 = cumulative_excess_returns2.iloc[-1]

# 计算年化超额收益率
annual_chaoerreturn_continuous_compounding2 = np.log(1 + chaoer_return2 ) / (total_days / 252)
annual_chaoerreturn_continuous_compounding_pct2 = (annual_chaoerreturn_continuous_compounding2 * 100)
print("超额收益率：", annual_chaoerreturn_continuous_compounding_pct2, "%")

## 计算超额收益率的标准差
chaoer_std2 = layer_excess_returns2.std()
chaoer_std2y = chaoer_std2 /math.sqrt(total_days / 252)
chaoer_std_pct2= (chaoer_std2y * 100).round(2) 
print("超额收益率标准差：", chaoer_std_pct2, "%")

## 计算夏普比率
sharp_ratio2 = annual_chaoerreturn_continuous_compounding_pct2 / chaoer_std_pct2
print("夏普比率:", sharp_ratio2 )
