# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 22:48:08 2021

@author: Loyal.Aujust
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

#读取sh000300和000905指数数据以及ETF单位净值数据
data000300 = pd.DataFrame(pd.read_csv('sh000300_Index_k_data.csv',header=0))
data000905 = pd.DataFrame(pd.read_csv('sh000905_Index_k_data.csv',header=0))

ETF=pd.DataFrame(pd.read_csv('ETF.csv',header=0))

initial_index = data000300[data000300.date=='2015-01-05'].index.tolist()
initial_index=initial_index[0]


global DataMatrix,Close_index2,Close_index8,ETF_Index
#提取大小盘收盘指数
Close_index2=data000300['close']
Close_index8=data000905['close']
#300ETF和500ETF
ETF2=ETF['510300.XSHG']
ETF8=ETF['510500.XSHG']
ETF_Index=pd.concat([ETF8,ETF2],axis=1)


#二八轮动策略并打印核实执行了何种操作
def strategy(Cash,Amount,Strands,Type,Date_Index):
    d300=(Close_index2[Date_Index]-Close_index2[Date_Index-20])/Close_index2[Date_Index]
    d500=(Close_index8[Date_Index]-Close_index8[Date_Index-20])/Close_index8[Date_Index]
    #更新金额
    if Type==-1:
        Amount=0
    else:  
        Amount=Strands*ETF_Index.iloc[Date_Index,Type]

        
    if d300<0 and Type==1:
        #000300下降趋势，卖出300ETF
        Cash=Amount
        Type=-1   #无持仓
        Strands=0
        Amount=0
        print(data000300['date'].iloc[Date_Index],'','Sell 300ETF')

    if d500<0 and Type==0:
        #000905下降趋势卖出500ETF
        Cash=Amount
        Type=-1   #无持仓
        Strands=0
        Amount=0
        print(data000300['date'].iloc[Date_Index],'','Sell 500ETF')
        
    if d300>d500 and d300>0 and Type != 1 and Amount==0:
        #000300上涨且幅度大于000905，买入300ETF
        Type=1
        Strands=Cash/ETF_Index.iloc[Date_Index,Type]
        Amount=Amount+Cash
        Cash=0
        print(data000300['date'].iloc[Date_Index],'','Buy 300ETF')

    if d300<d500 and d500>0 and Type != 0 and Amount==0:
        #000905上涨且幅度大于000300，买入500ETF
        Type=0
        Strands=Cash/ETF_Index.iloc[Date_Index,Type]
        Amount=Amount+Cash
        Cash=0
        print(data000300['date'].iloc[Date_Index],'','Buy 500ETF')
   
    return Cash,Amount,Strands,Type


#------------------------------------------------------------#
#初始化
Date=initial_index
stop=ETF_Index.shape[0]
#初始资金
cash=500000
amount=0
initial_asset=cash+amount
#买入500ETF
stype=0   #Type=0,1对应500ETF和300ETF
price500=ETF_Index.iloc[Date,stype]
strands=amount/price500    #不考虑手续费
Date=Date+1
d=1 #执行策略频率

#储存收益数据
DataMatrix=np.array([0])

#执行策略
while Date<stop:
    cash,amount,strands,stype=strategy(cash,amount,strands,stype,Date)
    asset=cash+amount
    #收益率
    ben=100*(asset-initial_asset)/initial_asset
    DataMatrix=np.append(DataMatrix,ben)
    # print(Date,cash,amount,strands,stype,ben)
    Date=Date+d
    
#计算000300和000905 index
index000300=Close_index2[initial_index:].values
index000905=Close_index8[initial_index:].values
index000300=100*(index000300-index000300[0])/index000300[0]
index000905=100*(index000905-index000905[0])/index000905[0]



#plot figure
plt.figure(1)
plt.rcParams['figure.dpi'] = 1000
plt.rcParams.update({'font.size': 8})

Date_list=data000300.iloc[initial_index:,0].to_list()
#绘制曲线
plt.plot(DataMatrix)
plt.plot(index000300)
plt.plot(index000905)
my_x_ticks = np.arange(initial_index,stop,200)
labels=data000300['date'].iloc[my_x_ticks]
plt.xticks(my_x_ticks,labels,rotation=30)  #设置x轴刻度
plt.yticks(np.arange(-10,160,10)) #设置y轴刻度
#图例
my_font=matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\simhei.ttf",size=7.0)
plt.legend(('二八轮动','沪深300指数','中证00指数'),prop=my_font)
#横纵坐标label
ax=plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
plt.xlabel('Time')
plt.ylabel('Yeild %')


#存储数据
index000300=pd.Series(index000300)
index000905=pd.Series(index000905)
p=pd.DataFrame(DataMatrix)
DataMatrix=pd.concat([p,index000300,index000905],axis=1).values

DataMatrix=pd.DataFrame(DataMatrix,index=Date_list,columns=['Strategy','沪深300','中证500'])
#Save 
DataMatrix.to_csv('D:\\BUAA\DataMatrix.csv',encoding='utf_8_sig')

