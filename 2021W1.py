import pandas as pd

data=pd.read_csv('data/PD 2021 Wk 1 Input - Bike Sales.csv')

##Split store-bike column into store and bike.
data[['Store','Bike']]=data['Store - Bike'].str.split('-',expand=True)
data['Bike']=data['Bike'].str.strip()

##Clean up the 'Bike' field to leave just three values in the 'Bike' field (Mountain, Gravel, Road)
bike_map={'Mountaen':'Mountain',
         'Rowd':'Road',
         'Rood':'Road',
         'Graval':'Gravel',
         'Gravle':'Gravel'}

data['Bike']=data['Bike'].map(bike_map).fillna(data['Bike'])
#Create two different cuts of the date field: 'quarter' and 'day of month'
data['Date']=pd.to_datetime(data['Date'],format='%d/%m/%Y')

data['quarter']=data['Date'].dt.quarter
data['day of month']=data['Date'].dt.day

#Remove the first 10 orders as they are test values
df=data[10:].drop(['Date','Store - Bike'],axis=1)

df.to_csv('output/PD 2021 W1 Output.csv',index=False)