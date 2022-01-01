# Prepping Data 2021 Week 48

import pandas as pd
import re

data=pd.read_excel('data/PD 2021 Wk 48 Input.xlsx')

def clean_data(df,value):

    df=pd.melt(df,id_vars=value,value_name='True Value',var_name='Recorded Year')
    df['Branch']=value
    df.rename(columns={value:'Clean Measure Names'},inplace=True)
    df['Recorded Year']=df['Recorded Year'].apply(lambda x:re.sub('Year','',x))
    df.loc[~(df['Clean Measure Names']=='Number of Staff'),'True Value']=df.loc[~(df['Clean Measure Names']=='Number of Staff'),].apply(lambda x:x['True Value']*1000000 if re.search('\((.)\)$',x['Clean Measure Names']).group(1)=='m'  else x['True Value']*1000 if re.search('\((.)\)$',x['Clean Measure Names']).group(1)=='k' else x['True Value'],axis=1)
    df['Clean Measure Names']=df['Clean Measure Names'].apply(lambda x:re.sub('\((.)\)$','',x))
    return df

#Extract each data table within the Excel workbook
lewisham=data.iloc[0:4,1:]
lewisham.columns=lewisham.iloc[0]
lewisham=lewisham[1:]

wimbledon=data.iloc[5:9,1:]
wimbledon.columns=wimbledon.iloc[0]
wimbledon=wimbledon[1:]

york=data.iloc[10:15,1:]
york.columns=york.iloc[0]
york=york[1:]

lewisham=clean_data(lewisham,'Lewisham')
wimbledon=clean_data(wimbledon,'Wimbledon')
york=clean_data(york,'York')

final=pd.concat([lewisham,wimbledon,york])

final=final[['Branch','Clean Measure Names','Recorded Year','True Value']]









#Extract the branch name from the table structure