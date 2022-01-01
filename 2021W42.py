# Prepping Data Week 42 2021

import pandas as pd

data=pd.read_csv('data/Prep Generate Rows datasets - Charity Fundraiser.csv')

data['Date']=pd.to_datetime(data['Date'],format='%d/%m/%Y')

data.index=pd.DatetimeIndex(data['Date'])

data=data.reindex(pd.date_range(data.index.min(),data.index.max()),
                    method='ffill').rename_axis('DateFill').reset_index()

data=data.sort_values('DateFill').rename_axis('Days into fund raising').reset_index()    

data['Value raised per day']=data.apply(lambda x:x['Total Raised to date']/x['Days into fund raising']
                                        if x['Days into fund raising']>0 else None,axis=1)

data['Date']=data['DateFill'].dt.strftime('%A')   

data['Average raised per weekday']=data['Value raised per day'].groupby(data['Date']).transform('mean')

