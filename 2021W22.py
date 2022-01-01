import pandas as pd
import numpy as np
import re

#Input the data:
answer_smash=pd.read_excel('data/PD 2021 Wk 22 Answer Smash Input.xlsx',sheet_name='Answer Smash')
names=pd.read_excel('data/PD 2021 Wk 22 Answer Smash Input.xlsx',sheet_name='Names')
questions=pd.read_excel('data/PD 2021 Wk 22 Answer Smash Input.xlsx',sheet_name='Questions')
category=pd.read_excel('data/PD 2021 Wk 22 Answer Smash Input.xlsx',sheet_name='Category')

#The category dataset requires some cleaning so that Category and Answer are 2 separate fields 
category[['Category','Answer']]=category['Category: Answer'].str.split(':',expand=True)
category['Answer']=category['Answer'].str.strip()
category.drop('Category: Answer',axis=1,inplace=True)
#Join the datasets together, making sure to keep an eye on row counts
j1=questions.merge(answer_smash,on='Q No',how='inner')
names['placeholder']=1
j1['placeholder']=1
j2=j1.merge(names,on='placeholder')
#Filter the data so that each answer smash is matched with the corresponding name and answer 
j2['check']=j2.apply(lambda x:1 if re.search(x['Name'],x['Answer Smash']) else 0,axis=1)
j2=j2[j2['check']==1].copy()
final=j2.merge(category,on='Category')
final['check']=final.apply(lambda x:1 if re.search(x['Answer'].lower(),x['Answer Smash'].lower()) else 0,axis=1)
final=final[final['check']==1].copy()

final=final[['Q No','Question','Answer','Name','Answer Smash']].copy()