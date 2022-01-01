import pandas as pd

#Input the data
data=pd.read_csv('data/PD 2021 Wk 5 Input.csv')

#For each Client, work out who the most recent Account Manager is

data_CAM=data.sort_values(by='From Date').groupby(['Client'])['Account Manager','Client ID'].last().reset_index()

#Filter the data so that only the most recent Account Manager remains
#Be careful not to lose any attendees from the training sessions!

data_dedup=data.drop_duplicates(subset=['Contact Email','Contact Name','Client','Training'])

result_a = data_dedup.merge(data_CAM,how='left',on=['Client'])

result_a.drop(['Client ID_x','Account Manager_x'],axis=1,inplace=True)
result_a.rename(columns={'Account Manager_y':'Account Manager','Client ID_y':'Client ID'},inplace=True)

result_a.to_csv('output/PD 2021 Wk 5 Output.csv',index=False)