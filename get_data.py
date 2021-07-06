# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 11:48:27 2021

@author: Loyal.Aujust
"""

import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
#沪深300
rs = bs.query_history_k_data_plus("sh.000300",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date='2014-12-01', end_date='2020-01-01', frequency="d")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
# 结果集输出到csv文件
result.to_csv("D:\\BUAA\sh000300_Index_k_data.csv", index=False)

#中证500
rs = bs.query_history_k_data_plus("sh.000905",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date='2014-12-01', end_date='2020-01-01', frequency="d")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
# 结果集输出到csv文件
result.to_csv("D:\\BUAA\sh000905_Index_k_data.csv", index=False)

# 登出系统
bs.logout()
