import pandas as pd

data=pd.read_excel('data/PD 2021 Wk 6 PGALPGAMoney2019.xlsx',sheet_name='OfficialMoney')
data['money per event']=data['MONEY']/data['EVENTS']
#What's the Total Prize Money earned by players for each tour?
total_price=data.groupby(['TOUR'])['MONEY'].sum().reset_index()
total_price['Measure']='Total Prize Money'
total_price=total_price.pivot_table(index='Measure',columns='TOUR',values='MONEY',aggfunc=max).reset_index()
#How many players are in this dataset for each tour?
total_players=data.groupby(['TOUR'])['PLAYER NAME'].nunique().reset_index()
total_players['Measure']='Number of Players'
total_players=total_players.pivot_table(index='Measure',columns='TOUR',values='PLAYER NAME',aggfunc=max).reset_index()
#How many events in total did players participate in for each tour?
total_events=data.groupby(['TOUR'])['EVENTS'].sum().reset_index()
total_events['Measure']='Number of Events'
total_events=total_events.pivot_table(index='Measure',columns='TOUR',values='EVENTS',aggfunc=max).reset_index()
#How much do players win per event? What's the average of this for each tour? 
avg_money_per_event=data.groupby(['TOUR'])['money per event'].mean().reset_index()
avg_money_per_event['Measure']='Avg Money per Event'
avg_money_per_event=avg_money_per_event.pivot_table(index='Measure',columns='TOUR',values='money per event',aggfunc=max).reset_index()
#How do players rank by prize money for each tour? What about overall? What is the average difference between where they are ranked within their tour compared to the overall rankings where both tours are combined?
data['RANK']=data.groupby(['TOUR'])['MONEY'].rank(ascending=False).astype(int)
data['OVERALL RANK']=data['MONEY'].rank(ascending=False).astype(int)
data['DIFF IN RANK']=data['OVERALL RANK']-data['RANK']
avg_diff_rank=data.groupby('TOUR')['DIFF IN RANK'].mean().reset_index()
avg_diff_rank['Measure']='Avg Difference in Ranking'
avg_diff_rank=avg_diff_rank.pivot_table(index='Measure',columns='TOUR',values='DIFF IN RANK',aggfunc=max).reset_index()

result_a=pd.concat([avg_diff_rank,avg_money_per_event,total_players,total_events,total_price],axis=0)

result_a['Difference between tours']=result_a['LPGA']-result_a['PGA']

result_a.to_csv('output/PD 2021 Wk 6 Output.csv',index=False)