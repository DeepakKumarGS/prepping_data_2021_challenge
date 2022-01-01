import pandas as pd

# Input the data
data1= pd.read_excel('data/PD 2021 Wk 8 Karaoke Dataset.xlsx',sheet_name='Karaoke Choices')
customers=pd.read_excel('data/PD 2021 Wk 8 Karaoke Dataset.xlsx',sheet_name='Customers')

#Calculate the time between songs
foo = data1.sort_values('Date').reset_index(drop=True)
foo['Song ID']=foo.index+1
#Calculate the time between songs
foo['Time between songs']=(foo['Date']-foo['Date'].shift(1)).astype('timedelta64[m]')
#If the time between songs is greater than (or equal to) 59 minutes, flag this as being a new session 
#Create a session number field
foo['Session Number']=foo.apply(lambda x:1 if x['Song ID']==1 or x['Time between songs']>=59 else 0,axis=1).cumsum()
#Number the songs in order for each session
foo['Song Number']=foo['Song ID']-foo['Song ID'].groupby(foo['Session Number']).transform('min')+1
#Match the customers to the correct session, based on their entry time 
first_entry=foo.groupby('Session Number',as_index=False)['Date'].min()
first_entry['Early Entry']=first_entry['Date'].apply(lambda x:x+pd.Timedelta(minutes=-10))
first_entry['temp']=1
customers['temp']=1
final=pd.merge(first_entry,customers,on='temp')
final=final[(final['Entry Time']<=final['Date']) & (final['Entry Time']>=final['Early Entry'])][['Session Number','Customer ID']]

final=pd.merge(foo,final,on='Session Number',how='left')
final.drop(['Song ID','Time between songs'],axis=1,inplace=True)

final.to_csv('output/PD 2021 Wk 8 Karaoke Output.csv',index=False)