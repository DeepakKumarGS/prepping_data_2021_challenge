import pandas as pd
import re
data=pd.read_csv('data/PD 2021 Wk 2 Input - Bike Model Sales.csv')

#Clean up the Model field to leave only the letters to represent the Brand of the bike
data['Brand']=data['Model'].apply(lambda x:re.sub('\d|\W','',x))

#Workout the Order Value using Value per Bike and Quantity.

data['Order Value']=data['Quantity'] * data['Value per Bike']

#Aggregate Value per Bike, Order Value and Quantity by Brand and Bike Type to form
#Quantity Sold
#Order Value
#Average Value Sold per Brand, Type

foo=data.groupby(['Brand','Bike Type'])['Quantity','Order Value'].sum().reset_index()
bar=data.groupby(['Brand','Bike Type'])['Value per Bike'].mean().reset_index()
bar.rename(columns={'Value per Bike':'Avg.Value per Bike'},inplace=True)
result_a=pd.merge(foo,bar,on=['Brand','Bike Type'])
result_a['Avg.Value per Bike']=round(result_a['Avg.Value per Bike'],1)

#Calculate Days to ship by measuring the difference between when an order was placed and when it was shipped as 'Days to Ship' 
data['Order Date']=pd.to_datetime(data['Order Date'],format='%d/%m/%Y')
data['Shipping Date']=pd.to_datetime(data['Shipping Date'],format='%d/%m/%Y')

data['days to ship']=(data['Shipping Date']-data['Order Date']).dt.days

#Aggregate Order Value, Quantity and Days to Ship by Brand and Store to form:
#Total Quantity Sold
#Total Order Value
#Average Days to Ship
foo=data.groupby(['Brand','Store'])['Quantity','Order Value'].sum().reset_index()
bar=data.groupby(['Brand','Store'])['days to ship'].mean().reset_index()
bar.rename(columns={'days to ship':'Avg.days to ship'},inplace=True)
result_b=pd.merge(foo,bar,on=['Brand','Store'])
result_b['Avg.days to ship']=round(result_b['Avg.days to ship'],1)

#Output datasets:
result_a.to_csv('output/PD 2021 W2 Brand Type.csv',index=False)
result_b.to_csv('output/PD 2021 W2 Brand Store.csv',index=False)