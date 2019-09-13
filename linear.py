import pandas as pd
from sklearn import linear_model
import math
import numpy as np
import matplotlib.pyplot as plt

#clear the data form
def spl(a):
    b=a.split('-')
    return int(b[0]+b[1]+b[2])

# compute accuracy
def accuracy(forecaste,true):
    b=min(abs(forecaste/true-1),0.8)
    return b

data=pd.read_csv("../data/Income Statement.csv")
ndata=data[["TICKER_SYMBOL","PUBLISH_DATE","END_DATE",'REPORT_TYPE','REVENUE']]
data_2=pd.read_csv("../data/FDDC_financial_submit_20180524.csv",names=['ticket'])
data_2c=data_2.copy()
for i in range(len(data_2)):
    data_2.loc[i,'ticket']=int(data_2.loc[i,'ticket'][0:6])

#print(ndata.head())
def get_data(index_1):
    new=ndata.loc[ndata['TICKER_SYMBOL']==index_1]
    totrain=pd.DataFrame(columns=["TICKER_SYMBOL","PUBLISH_DATE","END_DATE",'REPORT_TYPE','REVENUE'])
    totrain=totrain.append(ndata.loc[ndata['TICKER_SYMBOL']==index_1],ignore_index=True)
    # print(totrain)
    for i in range(0,len(totrain)):
        totrain.loc[i,"PUBLISH_DATE"]=spl(totrain.loc[i,"PUBLISH_DATE"])
        totrain.loc[i, "END_DATE"] = spl(totrain.loc[i, "END_DATE"])
    # print(totrain)
    train=pd.DataFrame(columns=["TICKER_SYMBOL","PUBLISH_DATE","END_DATE",'REPORT_TYPE','REVENUE'])
    for i in totrain['END_DATE']:
        publish=totrain.loc[totrain['END_DATE']==i]
        publish=publish.sort_values(by=["PUBLISH_DATE"],ascending=True)
        #print(publish.iloc[-1:])
        train=train.append(publish.iloc[-1],ignore_index=True)
    train.drop_duplicates("END_DATE",inplace=True)
    #print(train['REPORT_TYPE'].value_counts())
    train=train.sort_values(by="END_DATE")
    copy=pd.DataFrame(columns=["TICKER_SYMBOL","PUBLISH_DATE","END_DATE",'REPORT_TYPE','REVENUE'])
    copy=copy.append(train,ignore_index=True)

    #preserve the original data
    origin=copy.copy()
    # print("origin\n",origin)
    g = origin.loc[origin['REPORT_TYPE'] == 'S1']
    gro = pd.DataFrame(columns=["TICKER_SYMBOL", "PUBLISH_DATE", "END_DATE", 'REPORT_TYPE', 'REVENUE', "time"])
    gro = gro.append(g, ignore_index=True)
    gro["time"] = range(len(g))
    # print("gro的形式是:\n", gro)  ####观测df
    return gro, origin, copy

def get_groupdata(copy):
    #construct the data for linear regression
    i = 0
    while i<len(copy)-1:
        j=i+3
        while j>=i+1:
            copy.loc[j,'REVENUE']=copy.loc[j,'REVENUE']-copy.loc[j-1,'REVENUE']
            j-=1
        i+=4
    # print("单季度数据\n",copy)
    df=pd.DataFrame(columns=['train','time'])
    i=2
    k = 0
    while i<len(copy)-3:
        x=0
        for j in range(i,i+4):
            x=x+copy.loc[j,'REVENUE']
        df.loc[k]=[x,k]
        k+=1
        i+=4
    # print(df)
    return df

def get_linear(df,copy,origin):
    test=len(df)
    t=len(copy)
    regr=linear_model.LinearRegression()
    regr.fit(df['time'].reshape(-1,1),df['train'])
    a,b=regr.coef_,regr.intercept_
    devide=copy.loc[t-2,'REVENUE']+copy.loc[t-3,'REVENUE']#+copy.loc[t-3,'REVENUE']
    predevide=copy.loc[t-6,'REVENUE']+copy.loc[t-7,'REVENUE']#+copy.loc[t-6,'REVENUE']
    forecast=(a*test+b)-devide
    preforecast = (a * (test - 1) + b) - predevide
    acu=accuracy(preforecast,origin.loc[t-4,'REVENUE'])
    # print(acu,forecast)
    return forecast,acu

#linear regression by sum of group(4 seasons)
def get_linear_S1(gro,origin):
    test = len(gro)
    t=len(origin)
    regr=linear_model.LinearRegression()
    regr.fit(gro["time"].reshape(-1,1),gro['REVENUE'])
    a,b=regr.coef_,regr.intercept_
    forecast=(a*test+b)
    preforecast = (a * (test - 1) + b )
    acu=accuracy(preforecast,origin.loc[t-4,'REVENUE'])
    return forecast,acu

#linear regression by the growth rate of group sum
def get_growth(gro,origin):
    test = len(gro)
    t = len(origin)
    c=gro.copy()
    d=c.copy()
    i=test-1
    while i>0:
        c.loc[i,'REVENUE']=c.loc[i,'REVENUE']/c.loc[i-1,'REVENUE']
        i-=1
    c.loc[0,'REVENUE']=0
    # print(gro)
    regr = linear_model.LinearRegression()
    regr.fit(c["time"].reshape(-1, 1), c['REVENUE'])
    a, b = regr.coef_, regr.intercept_
    forecast = (a * test + b)*d.loc[test-1,'REVENUE']
    preforecast = (a * (test - 1) + b)*d.loc[test-2,'REVENUE']
    acu = accuracy(preforecast, origin.loc[t - 4, 'REVENUE'])
    return forecast, acu

b=0
flag=0
devide=1000000   #data unit is million
result=pd.DataFrame(columns=['TICKER_SYMBOL','REVENUE'])
for i in data_2['ticket']:
# for i in [1,5,6,9]:
    try:
        gro, origin, copy=get_data(i)
        forecast_1, acu_1 = get_growth(gro, origin)
        forecast_3, acu_3 = get_linear_S1(gro, origin)
    except KeyError:
        forecast_1,acu_1=0,0.8
        forecast_3, acu_3 = 0, 0.8
    except ValueError:
        forecast_1, acu_1 = 0, 0.8
        forecast_3, acu_3 = 0, 0.8
    try:
        df = get_groupdata(copy)
        fill=0
        forecast_2, acu_2 = get_linear(df, copy, origin)
        # print(forecast_1,acu_1)
    except KeyError:
        forecast_2,acu_2=0,0.8
    except ValueError:
        forecast_2, acu_2 = 0, 0.8
    if forecast_2>0 and forecast_1>0 and forecast_3>0:
        f=min(acu_3,acu_2,acu_1)
        if acu_2==f:
            result.loc[flag]=[str(i),round(float(forecast_2)/devide,2)]
        elif acu_1==f:
            result.loc[flag] = [str(i), round(float(forecast_1)/devide,2)]
        else:
            result.loc[flag] = [str(i), round(float(forecast_3)/devide,2)]
    elif forecast_3>0:
        result.loc[flag] = [str(i), round(float(forecast_3)/devide,2)]
    elif forecast_1>0:
        result.loc[flag] = [str(i), round(float(forecast_1)/devide,2)]
    elif forecast_2 > 0:
        result.loc[flag] = [str(i), round(float(forecast_2)/devide,2)]
    else:
        result.loc[flag]=[str(i),fill]
    flag += 1
x=round(result['REVENUE'].mean(),2)
result['REVENUE']=result['REVENUE'].replace(0,x)
result['TICKER_SYMBOL']=data_2c['ticket']
# print(x)
result.to_csv("result.csv",index=False,header=None)
