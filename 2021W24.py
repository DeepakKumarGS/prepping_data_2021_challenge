## Prepping Data 2021 Week 24
# Inspiration - Kelly Gilbert 
#https://github.com/kelly-gilbert/preppin-data-challenge/tree/master/2021/preppin-data-2021-24
import pandas as pd
#Input data
absence=pd.read_excel('data/PD 2021 Wk24 Absenteeism Scaffold.xlsx',sheet_name='Reasons')
scaffold=pd.read_excel('data/PD 2021 Wk24 Absenteeism Scaffold.xlsx',sheet_name='Scaffold')

start_date='2021-04-01'
end_date='2021-05-31'
#Build a data set that has each date listed out between 1st April to 31st May 2021
scaffold['Date']=pd.date_range(start_date,end_date)
#Build a data set containing each date someone will be off work

absence['Date']=[pd.date_range(d,periods=p,freq='D') for d,p in zip(absence['Start Date'],absence['Days Off'])]
#Workout the number of people off each day
absence_count=absence.explode('Date').groupby('Date')['Name'].count().reset_index().rename(columns={'Name':'Number of people off each day'})

#Merge the datasets
data=pd.merge(scaffold,absence_count,on='Date',how='left')
data.fillna(0,inplace=True)
#Output the data
data.to_csv('output/PD 2021 Wk24 Output.csv',index=False)

#What date had the most people off?
data.iloc[data.iloc[:,2].idxmax()]['Date']
#How many days does no-one have time off on?
len(data.loc[data['Number of people off each day']==0])



