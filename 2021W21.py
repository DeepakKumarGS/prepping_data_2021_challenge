import pandas as pd
import numpy as np
import re
#Input the data:
xls_file = pd.ExcelFile('data/PD 2021 Wk 21 Input.xlsx')
temp=[]
for sheet in [sh for sh in xls_file.sheet_names]:
    df=pd.read_excel(xls_file,sheet_name=sheet)
    df['Month']=sheet
    temp.append(df)
data=pd.concat(temp)

data['Destination']=data['Destination'].str.strip()

data['Month']=data['Month'].apply(lambda x:re.sub('Month','',x)).astype('str')

data['Year']='2021'

data['Date']=pd.to_datetime(data['Day of Month'].astype('str')+'-'+data['Month']+'-'+data['Year'])

data['New Trolley Inventory?']=np.where(data['Date']>='2021-06-01','TRUE','FALSE')

data['Product']=data['Product'].apply(lambda x:re.search('(\w+)\s(?=-)',x).group(1) if re.search('(\w+)\s(?=-)',x) else x)

data['Price']=data['Price'].str.replace('$','').astype('float32')

data['Avg Price per Product']=data.groupby('Product')['Price'].transform('mean')

data['Variance']=data['Price']-data['Avg Price per Product']

data['Variance Rank by Destination']=data.groupby(['Destination','New Trolley Inventory?'])['Variance'].rank(ascending=False).astype('int')

final = data.loc[data['Variance Rank by Destination']<=5,['New Trolley Inventory?',
                                                            'Variance Rank by Destination',
                                                            'Variance',
                                                            'Avg Price per Product',
                                                            'Date',
                                                            'Product',
                                                            'first_name',
                                                            'last_name',
                                                            'email',
                                                            'Price',
                                                            'Destination']]

final.to_csv('output/PD 2021 W21 Output(Process).csv',index=False)