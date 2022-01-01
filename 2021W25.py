## Prepping Data Week 25 2021

## Inspiration - Arsene Xie (@ArseneXie)
import xlrd
import pandas as pd
import numpy as np
import re

xls_sheet=xlrd.open_workbook('data/PD 2021 W25 Input.xlsx')

for index,sheet_name in enumerate(xls_sheet.sheet_names()):
    globals()['data%s' %index]=pd.read_excel('data/PD 2021 W25 Input.xlsx',sheet_name=sheet_name)

#Clean up the list of Gen 1 Pokémon so we have 1 row per Pokémon
data0=data0[['#','Name']].dropna()
#Clean up the Evolution Group input so that we can join it to the Gen 1 list 
#Filter out Starter and Legendary Pokémon
data1=data1.loc[((data1['Starter?']==0) & (data1['Legendary?']==0)),['Evolution Group','#']]
data1['#']=data1['#'].apply(lambda x:int(x.strip()))

gen=pd.merge(data0,data1,on='#').drop('#',axis=1)

#Using the Evolutions input, exclude any Pokémon that evolves from a Pokémon that is not part of Gen 1 or can evolve into a Pokémon outside of Gen 1
data2=data2[['Evolving from','Evolving to']]
evo_from=pd.merge(data2,gen,left_on='Evolving from',right_on='Name')[['Evolution Group','Evolving to']].rename(columns={'Evolving to':'Pokemon'})
evo_to=pd.merge(data2,gen,left_on='Evolving to',right_on='Name')[['Evolution Group','Evolving from']].rename(columns={'Evolving from':'Pokemon'})

df=pd.concat([evo_from,evo_to]).drop_duplicates()
#Exclude any Pokémon with a mega evolution, Alolan, Galarian or Gigantamax form
exc_evo=pd.concat([data3,data4,data5,data6])
exc_evo['Name']=exc_evo['Name'].apply(lambda x:re.sub('^\w+\s','',x))

df['is_form']=df['Pokemon'].isin(list(exc_evo['Name'])).astype(int)

df['Group Form']=df['is_form'].groupby(df['Evolution Group']).transform('sum')

df=df.loc[df['Group Form']==0,['Evolution Group','Pokemon']]

#It's not possible to catch certain Pokémon in the most recent games. These are the only ones we will consider from this point on
data7.rename(columns={'Name':'Evolution Group'},inplace=True)
df=pd.merge(df,data7,on='Evolution Group')
df=pd.merge(df,data8,on='Pokemon')
#We're left with 10 evolution groups. Rank them in ascending order of how many times they've appeared in the anime to see who the worst Pokémon is!

df=df.groupby('Evolution Group',as_index=False).agg(Appearances=('Episode','nunique'))
df['The Worst Pokemon']=df['Appearances'].rank(method='min').astype(int)

df=df.sort_values('Appearances')
#Output the data
df.to_csv('PD 2021 Wk25 Solution.csv',index=False)



