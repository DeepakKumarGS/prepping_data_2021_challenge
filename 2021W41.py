# Prepping Data Week 41 2021

import pandas as pd
import numpy as np
import re

data=pd.read_csv('data/PD 2021 Wk41 Southend Stats.csv',sep="\s+")

data.rename(columns={'P.1':'Pts'},inplace=True)

data['Special Circumstances']=data.apply(lambda x:'Incomplete' if x['SEASON']==data['SEASON'].max() else
                                        'Abandoned due to WW2' if x['SEASON'][0:4]=='1939' else 'N/A',axis=1)

data['POS']=data.apply(lambda x:x['POS'] if x['Special Circumstances']=='N/A'else None,axis=1)

data['League Num']=data['LEAGUE'].apply(lambda x:0 if x=='FL-CH' else 5 if x=='NAT-P' else int(re.search('(\d)',x).group(1)))

data['Outcome Key']=data['League Num']-data['League Num'].shift(-1)

data['Outcome']=data['Outcome Key'].apply(lambda x:'Promoted' if x>0 else 'Relegated' if x<0 else 'Same League' if x==0 else None)

data.index=data['SEASON'].apply(lambda x:int(x[0:4]))


