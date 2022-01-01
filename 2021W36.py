import pandas as pd
import numpy as np
import re

timeline=pd.read_excel('data/Trend Input.xlsx',skiprows=2,sheet_name='Timeline')
country=pd.read_excel('data/Trend Input.xlsx',skiprows=2,sheet_name='Country Breakdown').dropna()

country=pd.melt(country,id_vars=['Country'],value_name='Percentage Value',value_vars=country.columns[1:],var_name='Trending')
country['Trending']=country['Trending'].apply(lambda x:re.sub('(:.*)','',x))
country=country.loc[country.reset_index().groupby('Trending')['Percentage Value'].idxmax()][['Trending','Country']]


timeline=pd.melt(timeline,id_vars=['Week'],value_vars=timeline.columns[1:],value_name='TrendingValue',var_name='Trending')
timeline['Trending']=timeline['Trending'].apply(lambda x:re.sub('(:.*)','',x))

timeline['avg index']=timeline.groupby('Trending')['TrendingValue'].transform('mean')
timeline['Index Peak']=timeline.groupby('Trending')['TrendingValue'].transform('max')
timeline['Index Peak Week']=timeline.apply(lambda x:x['Week'] if x['Index Peak']==x['TrendingValue'] else max(timeline['Week']),axis=1)
timeline['First Peak']=timeline['Index Peak Week'].groupby(timeline['Trending']).transform('min')
timeline['Year']=timeline['Week'].apply(lambda x:x.year+1 if x.month>=9 else x.year)

timeline=timeline[timeline['Year']>=max(timeline['Year']-1)].copy()
timeline['YearValue']=timeline['Year'].apply(lambda x:f'{str(x-1)}/{str(x)[2:]} avg index')

timeline=timeline.drop(['Week','Index Peak Week','Year'],axis=1)

final=timeline.pivot_table(index=[c for c in timeline.columns if c not in ['TrendingValue','YearValue']],
                            columns='YearValue',values='TrendingValue',aggfunc='mean').reset_index()

final['Status']=final.apply(lambda x:'Still Trendy' if x['2019/20 avg index']>=x['2020/21 avg index'] else 'Lockdown Fad',axis=1)

final=final.merge(country,on='Trending').rename(columns={'Country':'Country with highest percentage','Trending':'SearchTerm'})

final=final.drop('2019/20 avg index',axis=1)







