## Prepping Data Week 37
## Inspiration - Arsene @arsenexie

# Input the Data
# Calculate the End Date for each contract
# Create a Row for each month a person will hold the contract
# Calculate the monthly cumulative cost of each person's contract
# Output the Data

import pandas as pd
import numpy as np

data=pd.read_excel('data/2021 Week 37 Input.xlsx',sheet_name='Contract Details')

data=data.iloc[np.repeat(np.arange(len(data)),list(data['Contract Length (months)']))].copy()
data['rownum']=data.groupby('Name')['Start Date'].rank(method='first')

data['Payment Date']=data.apply(lambda x:(x['Start Date']+pd.DateOffset(months=x['rownum']-1)).date(),axis=1)

data['Cumulative Monthly Cost']=data['Monthly Cost'] * data['rownum']

final=data[['Name','Payment Date','Monthly Cost','Cumulative Monthly Cost']]

