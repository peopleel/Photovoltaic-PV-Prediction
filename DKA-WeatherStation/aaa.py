import os
import random
import pandas as pd
import numpy as np
import math 
import matplotlib.pyplot as plt

from pandas import read_csv
from math import sqrt

read_dataset = pd.read_csv('101-Site_DKA-WeatherStation.csv')

strsplit = read_dataset.Timestamp.str.split(expand = True)
strsplit.rename(columns={0:'date',1:'time'},inplace=True)
date = strsplit.date.str.split(expand = True,pat='/')
date.rename(columns={0:'Year',1:'Month',2:'Day'},inplace=True)
time = strsplit.time.str.split(expand = True,pat=':')
#time.rename(columns = {0:'H',1:'M',2:'S'},inplace = True)
time.rename(columns = {0:'Hour',1:'Minutes'},inplace = True)
read_dataset = pd.concat([read_dataset,date,time],axis=1)

read_dataset.rename(columns={
       'DKA.WeatherStation - Wind Speed (m/s)':'WS',
       'DKA.WeatherStation - Weather Temperature Celsius (°C)':'TC',
       'DKA.WeatherStation - Weather Relative Humidity (%)':'RH',
       'DKA.WeatherStation - Global Horizontal Radiation (W/m²)':'GHR',
       'DKA.WeatherStation - Diffuse Horizontal Radiation (W/m²)':'DHR',
       'DKA.WeatherStation - Wind Direction (Degrees)':'WD',
       'DKA.WeatherStation - Weather Daily Rainfall (mm)':'DR',
       'DKA.WeatherStation - Radiation Global Tilted (W/m²)':'RGT',
       'DKA.WeatherStation - Radiation Diffuse Tilted (W/m²)':'RDT',
       'DKA.WeatherStation - Wind Speed (m/s).1':'WS',
           },inplace=True)

dataset = read_dataset[['Timestamp','Year', 'Month',
       'Day', 'Hour', 'Minutes', 'WS', 'TC', 'RH', 'GHR', 'DHR', 'WD', 'DR', 'RGT', 'RDT',
       'WS']]

dataset_GHR = read_dataset[['Year', 'Month',
       'Day', 'Hour', 'Minutes','GHR']]

# #数据类型转换
dataset_GHR[['Year', 'Month','Day','Hour','Minutes']] = dataset_GHR[['Year', 'Month','Day','Hour','Minutes']].astype(int)
#丢弃
dataset_GHR = dataset_GHR.drop(dataset_GHR[(dataset_GHR.Hour < 7) | (dataset_GHR.Hour > 19)].index)

#数据类型还原
# dataset_GHR[['Year', 'Month','Day','Hour','Minutes']] = dataset_GHR[['Year', 'Month','Day','Hour','Minutes']].astype(object)

year_list = list(['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'])

month_list = list(['1','2','3','4','5','6','7','8','9','10','11','12'])

day_list = list(['1','2','3','4','5','6','7','8','9','10','11','12','13','14',
                '15','16','17','18','19','20','21','22','23','24','25','26','27',
                '28'])
###由于2009年2月28日 没有29，30，31 导致2009年3月写入程序跳出循环

hour_list = list(['7','8','9','10','11','12','13','14','15','16','17','18','19'])

minutes_list = list(['0','5','10','15','20','25','30','35','40','45','50','55'])

##扩展 列名  小时+分钟
hour_minutes=list()
for i in range(0, len(hour_list)):
    for j in range(0, len(minutes_list)):
        hour_minutes += [('%s:%s' % (hour_list[i],minutes_list[j]) )]
     
year_month_day=list()
for x in range(0, len(year_list)):
    for y in range(0, len(month_list)):
        for z in range(0, len(day_list)):
            year_month_day += [('%s/%s/%s' % (year_list[x],month_list[y],day_list[z]))]

colum = ['Timestamp','Year','Month','Day'] + hour_minutes 

newdata = pd.DataFrame(columns=colum)

for i in year_month_day:
    ymdsplit = i.split('/')
    year = int(ymdsplit[0])
    month = int(ymdsplit[1])
    day = int(ymdsplit[2])
    newdata = newdata.append(pd.DataFrame({'Timestamp':i,'Year':[year],'Month':[month],'Day':[day]}),ignore_index=False,sort=False)
    for j in hour_minutes:
        hmsplit = j.split(':')
        hour = int(hmsplit[0])
        minutes = int(hmsplit[1])
        ghr = dataset_GHR.loc[(dataset_GHR['Year'] == year ) & 
                      (dataset_GHR['Month'] == month )& 
                      (dataset_GHR['Day'] == day )& 
                      (dataset_GHR['Hour'] == hour )& 
                      (dataset_GHR['Minutes'] == minutes ),'GHR']
        ghr = ghr.values
        newdata.loc[(newdata['Year'] == year ) & 
                    (newdata['Month'] == month )& 
                    (newdata['Day'] == day ),j]=ghr


newdata.to_csv('./2009-2018按天辐照度.csv',index=False)


