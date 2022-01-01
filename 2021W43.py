# Prepping data Week 43 2021

import pandas as pd
import datetime

bua=pd.read_excel('data/2021W43 Input.xlsx',sheet_name='Business Unit A ')

bub=pd.read_excel('data/2021W43 Input.xlsx',sheet_name='Business Unit B ',skiprows=5)
bub['Date lodged']=pd.to_datetime(bub['Date lodged'],format='%d/%m/%Y')

risk_level=pd.read_excel('data/2021W43 Input.xlsx',sheet_name='Risk Level')

bua['Date lodged']=bua.apply(lambda x:f"{x['Date']}/{x['Month ']}/{x['Year']}",axis=1)
bua['Date lodged']=pd.to_datetime(bua['Date lodged'],format='%d/%m/%Y')

risk_dict=risk_level.set_index('Risk level')['Risk rating'].T.to_dict()

bua['Rating']=bua['Rating'].map(risk_dict)

bua.drop(['Year','Month ','Date'],axis=1,inplace=True)
bua=bua[['Ticket ID', 'Business Unit ', 'Owner', 'Issue ', 'Management Strategy',
        'Date lodged','Status', 'Rating']].rename(columns={'Business Unit ':'Unit'})

bu=pd.concat([bua,bub])

bu['status by date lodged']=bu['Date lodged'].apply(lambda x:'Opening Cases' if x<datetime.date(2021,10,1) else 'New cases')

bu=bu[['Rating','Date lodged','Status','status by date lodged']].melt(id_vars=['Rating','Date lodged'],value_name='Status',var_name='delete').drop('delete',axis=1)

bu=bu.pivot_table(index='Rating',columns='Status',values='Date lodged',aggfunc='count').reset_index().fillna(0).rename(columns={'In Progress':'Continuing'})

bu=bu.melt(id_vars='Rating',value_name='Cases',var_name='Status').sort_values(['Rating','Status'])



