# Prepping Data 2021 Week 30

import pandas as pd

#Input the data
data=pd.read_csv('data/PD 2021 Wk30.csv')

data=data.sort_values(['Hour','Minute'],ascending=[True,True]).reset_index(drop=True)

#Create a TripID field based on the time of day
data['Date']=pd.to_datetime('2021-07-12',format='%Y-%m-%d').date()
data['time']=pd.to_datetime(data['Hour'].astype('str')+':'+data['Minute'].astype('str'),format='%H:%M').dt.time

data['Time']=pd.to_datetime(data['Date'].astype('str')+" "+data['time'].astype('str'))

data.drop(['Date','time'],inplace=True,axis=1)

data['TripID']=data['Time'].index

data=data.replace({'From':{'G':0,'B':-1},'To':{'G':0,'B':-1}})

data['From']=data['From'].astype('int')
data['To']=data['To'].astype('int')
#Calculate how many floors the lift has to travel between trips
data['Floor Btw Trips']=abs(data['From']-data['To'].shift(1))
#Calculate which floor the majority of trips begin at - call this the Default Position
data['Default Position']=data.groupby('From').count().Hour.idxmax()

#If every trip began from the same floor, how many floors would the lift need to travel to begin each journey?
data['From Default Position']=abs(data['From']-data['Default Position'])

lift=data.groupby('Default Position',as_index=False).agg({'From Default Position':'mean','Floor Btw Trips':'mean'})

lift['Difference']=lift['From Default Position']-lift['Floor Btw Trips']