import numpy as np
import pandas as pd


def get_gp_xy(basic_data, train_long):
    data = basic_data.drop(columns=['return', 'return+-1'])
    data = data.values
    target = basic_data['return'].values
    target_ = basic_data['return+-1'].values
    gp_x = np.nan_to_num(data)
    gp_y = np.nan_to_num(target_)

    X_train = np.nan_to_num(data[:train_long])
    Y_train = np.nan_to_num(target[:train_long])

    X_test = np.nan_to_num(data[train_long:])
    Y_test = np.nan_to_num(target[train_long:])

    X_train_ = np.nan_to_num(data[:train_long])
    Y_train_ = np.nan_to_num(target_[:train_long])

    return gp_x, gp_y, X_train_, Y_train_, X_train, Y_train, X_test, Y_test


def protected_division(x1, x2):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.abs(x2) > 0.001, np.divide(x1, x2), 1.)


def protected_sqrt(x1):
    return np.sqrt(np.abs(x1))


def protected_log(x1):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.abs(x1) > 0.001, np.log(np.abs(x1)), 0.)


def protected_inverse(x1):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.abs(x1) > 0.001, 1. / x1, 0.)


def sigmoid(x1):
    with np.errstate(over='ignore', under='ignore'):
        return 1 / (1 + np.exp(-x1))


# 相加
def gp_add(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return np.add(data1, data2)


# 相减
def gp_sub(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return np.subtract(data1, data2)


# 相乘
def gp_mul(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return np.multiply(data1, data2)


# 相除
def gp_div(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return protected_division(data1, data2)


# 两数比大小，取大值
def gp_max(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return np.maximum(data1, data2)


# 两数比大小，取小值
def gp_min(data1, data2):
    if isinstance(data1, float):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, float):
        data2 = np.repeat(data2, gp_x.shape[0])
    if isinstance(data1, int):
        data1 = np.repeat(data1, gp_x.shape[0])
    if isinstance(data2, int):
        data2 = np.repeat(data2, gp_x.shape[0])
    return np.minimum(data1, data2)


# 绝对值平方根
def gp_sqrt(data):
    if isinstance(data, float):
        return protected_sqrt(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return protected_sqrt(np.repeat(data, gp_x.shape[0]))
    return protected_sqrt(data)


# 对数
def gp_log(data):
    if isinstance(data, float):
        return protected_log(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return protected_log(np.repeat(data, gp_x.shape[0]))
    return protected_log(data)


# 取相反数
def gp_neg(data):
    if isinstance(data, float):
        return np.negative(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.negative(np.repeat(data, gp_x.shape[0]))
    return np.negative(data)


# 近零的参数返回0
def gp_inv(data):
    if isinstance(data, float):
        return protected_inverse(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return protected_inverse(np.repeat(data, gp_x.shape[0]))
    return protected_inverse(data)


# 取绝对值
def gp_abs(data):
    if isinstance(data, float):
        return np.abs(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.abs(np.repeat(data, gp_x.shape[0]))
    return np.abs(data)


# 三角函数
def gp_sin(data):
    if isinstance(data, float):
        return np.sin(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.sin(np.repeat(data, gp_x.shape[0]))
    return np.sin(data)


# 三角函数
def gp_cos(data):
    if isinstance(data, float):
        return np.cos(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.cos(np.repeat(data, gp_x.shape[0]))
    return np.cos(data)


# 三角函数
def gp_tan(data):
    if isinstance(data, float):
        return np.tan(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.tan(np.repeat(data, gp_x.shape[0]))
    return np.tan(data)


# 三角函数
def gp_sig(data):
    if isinstance(data, float):
        return sigmoid(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return sigmoid(np.repeat(data, gp_x.shape[0]))
    return sigmoid(data)


def rolling_prod(data):
    if isinstance(data, float):
        return np.prod(np.repeat(data, gp_x.shape[0]))
    if isinstance(data, int):
        return np.prod(np.repeat(data, gp_x.shape[0]))
    return np.prod(data)


# 数组10日移动窗口和
def ts_sum(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(window).sum().tolist())
    value = np.nan_to_num(value)
    return value


# 数组的10日移动平均数
def sma(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(window).mean().tolist())
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口标准差
def stddev(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(window).std().tolist())
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口元素相乘
def product(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(10).apply(rolling_prod).tolist())
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口最小值
def ts_min(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(window).min().tolist())
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口最小大值
def ts_max(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = np.array(pd.Series(data.flatten()).rolling(window).max().tolist())
    value = np.nan_to_num(value)
    return value


# 数组相邻两数差
def delta(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    value = np.diff(data.flatten())
    value = np.append(0, value)
    return value


# 往后移一个单位
def delay(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    period = 1
    value = pd.Series(data.flatten()).shift(1)
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口最大值索引
def ts_argmax(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = pd.Series(data.flatten()).rolling(10).apply(np.argmax) + 1
    value = np.nan_to_num(value)
    return value


# 数组10日移动窗口最小值索引
def ts_argmin(data):
    if isinstance(data, float):
        return np.repeat(data, gp_x.shape[0])
    if isinstance(data, int):
        return np.repeat(data, gp_x.shape[0])
    window = 10
    value = pd.Series(data.flatten()).rolling(10).apply(np.argmin) + 1
    value = np.nan_to_num(value)
    return value
