# Prepping Data 2021 W26
# Inspiration - Arsene Xie (@arseneXie)
#Input the data,
import pandas as pd

data=pd.read_csv('data/PD 2021 Wk 26 Input - Sheet1.csv')

#Create a data set that gives 7 rows per date (unless those dates aren't included in the data set). 
#ie 1st Jan only has 4 rows of data (1st, 2nd, 3rd & 4th)

data['Date']=pd.to_datetime(data['Date'],format='%d/%m/%Y')

data=data.groupby('Destination').apply(lambda x:x.sort_values('Date')).reset_index(drop=True)

rev_sum=data.groupby('Date',as_index=False).agg({'Revenue':'sum'})

rev_sum['Destination']='All'

prep=pd.concat([data,rev_sum])

# Create the Rolling Week Total and Rolling Week Average per destination
# Records that have less than 7 days data should remain included in the output

prep['Rolling Avg']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.rolling(7,1).mean().shift(-3))

# prep['Shift_3']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.shift(-3))

# prep['rolling_7']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.rolling(7,1))

# prep['rolling_7_mean']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.rolling(7,1).mean())

prep['Rolling Total']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.rolling(7,1).sum().shift(-3))

prep['Rolling Avg1']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.shift(-3).rolling(7,1).mean())

prep['Rolling Total1']=prep.groupby('Destination')['Revenue'].transform(lambda x:x.shift(-3).rolling(7,1).sum())
#Create the Rolling Week Total and Rolling Week Average for the whole data set
prep['Rolling Week Avg']=prep.apply(lambda x:x['Rolling Avg1'] if pd.isna(x['Rolling Avg']) else x['Rolling Avg'],axis=1)

prep['Rolling Week Total']=prep.apply(lambda x:x['Rolling Total1'] if pd.isna(x['Rolling Total']) else x['Rolling Total'],axis=1)

final=prep[['Destination','Date','Rolling Week Avg','Rolling Week Total']]



