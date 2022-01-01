# Prepping Data Week 38 2021
import pandas as pd
import re
import numpy as np

#Input the data
trilogy=pd.read_excel('data/Trilogies Input.xlsx',sheet_name='Top 30 Trilogies')
films=pd.read_excel('data/Trilogies Input.xlsx',sheet_name='Films')

#Remove the word trilogy from trilogy field
trilogy['Trilogy']=trilogy['Trilogy'].apply(lambda x:re.sub('trilogy','',x))

#Split out the Number in Series field into Film Order and Total Films in Series
films['Film Order']=films['Number in Series'].apply(lambda x:x.split('/')[0])
films['Total Films in Series']=films['Number in Series'].apply(lambda x:x.split('/')[1])

#Work out the average rating for each trilogy
films['Trilogy Average']=films.groupby('Trilogy Grouping')['Rating'].transform('mean')

#Work out the highest ranking for each trilogy
films['Highest Rank']=films.groupby('Trilogy Grouping')['Rating'].transform('max')

#Rank the trilogies based on the average rating and use the highest ranking metric to break ties (make sure you haven't rounded the numeric fields yet!)
films['Trilogy Ranking']=films.sort_values(['Trilogy Average','Highest Rank'],ascending=False).groupby(['Trilogy Average','Highest Rank'],sort=False).ngroup()+1

#Bring the 2 datasets together by the ranking fields
final=pd.merge(trilogy,films,how='inner',on='Trilogy Ranking')

final['Trilogy Average']=np.round(final['Trilogy Average'],1)

final=final[['Trilogy Ranking','Trilogy','Trilogy Average','Film Order','Title','Rating','Total Films in Series']]