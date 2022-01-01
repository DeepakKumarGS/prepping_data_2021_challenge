# Prepping Data 2021 Week 40

import pandas as pd

data=pd.read_csv('data/PD 2021 Wk40 Austin_Animal_Center_Outcomes.csv')
#Remove the duplicated date field
data.drop('MonthYear',axis=1,inplace=True)
#Filter to only cats and dogs (the other animals have too small a data sample)
data=data.loc[data['Animal Type'].isin(['Cat','Dog'])]
# Group up the Outcome Type field into 2 groups:
# Adopted, Returned to Owner or Transferred
# Other
data['Outcome Type']=data['Outcome Type'].replace(['Adoption','Transfer','Return to Owner'],'Adopted, Returned to Owner or Transferred')

#Calculate the % of Total for each Outcome Type Grouping and for each Animal Type
data.loc[~(data['Outcome Type']=='Adopted, Returned to Owner or Transferred'),'Outcome Type']='Other'

data['Rows']=1

final=data.groupby(['Animal Type','Outcome Type']).agg({'Rows':'sum'})

final['Ratio']=final['Rows'].groupby(level=0).apply(lambda x:round(x*100/float(x.sum()),1))

final=final.reset_index(drop=True)
#Output the data
final=final.pivot_table(index='Animal Type',columns='Outcome Type',values='Ratio',aggfunc=max).reset_index()


