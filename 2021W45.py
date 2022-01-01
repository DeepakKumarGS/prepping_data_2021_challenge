# Prepping Data 2021 Week 45
import pandas as pd
import xlrd
import re

def make_date(df,id):
    """
    function to create timestamp and the date field
    """

    df['Session Time']=df['Session Time'].apply(lambda x:re.search('(\d+:\d+)',f'{x}:00').group(1))
    if id==0:
        df['Date']='2021-11-10'
    elif id==1:
        df['Date']='2021-11-11'
    elif id==2:
        df['Date']='2021-11-12'
    df['Date']=df.apply(lambda x:pd.to_datetime(x['Date']+' '+x['Session Time'],format='%Y-%m-%d %H:%M'),axis=1)
    df.drop('Session Time',axis=1,inplace=True)
    return df

xls_doc=xlrd.open_workbook('data/PD 2021 Wk45 TC Input.xlsx')


for index,sheetname in enumerate(xls_doc.sheet_names()):
    print(f'{index}')
    globals()["data%s" %index]=pd.read_excel('data/PD 2021 Wk45 TC Input.xlsx',sheet_name=sheetname)
    globals()["data%s" %index]["Date"]=sheetname
    if sheetname!='Attendees':
        globals()["data%s" %index]=make_date(globals()["data%s" %index],index)

data=pd.concat([data0,data1,data2])

data3.rename(columns={'Attendee ID':'Attendee IDs'},inplace=True)

data3.drop('Date',axis=1,inplace=True)

data=data.set_index(['Session ID','Subject','Date']).apply(lambda x:x.str.split(',').explode()).reset_index()

data['Attendee IDs']=data['Attendee IDs'].astype('int64')

data=data.merge(data3,on='Attendee IDs',how='inner')

direct=data.merge(data[['Session ID','Attendee']].rename(columns={'Attendee':'Contact'}),on='Session ID')

direct=direct[direct['Attendee']!=direct['Contact']].copy()

direct['Contact Type']='Direct Contact'

indirect=pd.merge(direct.rename(columns={'Contact':'Direct Contact'}),
                    direct[['Date','Subject','Attendee','Contact']].rename(columns={'Attendee':'Direct Contact','Date':'PreviousDatetime'}),
                    on=['Subject','Direct Contact'])

indirect=indirect.query('`Date`>`PreviousDatetime`')

indirect=indirect[indirect['Attendee']!=indirect['Contact']].copy()

indirect['Contact Type']='Indirect Contact'

final=pd.concat([direct[['Subject','Attendee','Contact Type','Contact']],
                indirect[['Subject','Attendee','Contact Type','Contact']]])

final['idx']=final.groupby(['Subject','Attendee','Contact'])['Contact Type'].rank(method='first',ascending=True)

final=final[final['idx']==1].drop('idx',axis=1)



    