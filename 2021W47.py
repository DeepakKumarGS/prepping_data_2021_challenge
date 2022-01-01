# Prepping Data 2021 Week 47 

import pandas as pd
import numpy as np
event=pd.read_excel('data/PD 2021 Wk 47 top_female_poker_players_and_events.xlsx',sheet_name='top_100')

player=pd.read_excel('data/PD 2021 Wk 47 top_female_poker_players_and_events.xlsx',sheet_name='top_100_poker_events')

#Add the player names to their poker events
data=player.merge(event,on='player_id')
#Create a column to count when the player finished 1st in an event
data['first']=np.where(data['player_place']=='1st',1,0)
#Replace any nulls in prize_usd with zero
data['prize_usd'].fillna(0,inplace=True)
#Find the dates of the players first and last events
data['min_date']=data.groupby('player_id',as_index=False)['event_date'].transform('min')
data['max_date']=data.groupby('player_id',as_index=False)['event_date'].transform('max')
#Use these dates to calculate the length of poker career in years (with decimals)
data['career_length']=(data['max_date']-data['min_date']).dt.days/365
#Create an aggregated view to find the following player stats:
# Number of events they've taken part in
# Total prize money
# Their biggest win
# The percentage of events they've won
# The distinct count of the country played in
# Their length of career
data['number_of_events']=data.groupby('player_id',as_index=False)['event_name'].transform('count')
data['total_prize_money']=data.groupby('player_id',as_index=False)['all_time_money_usd'].transform('max')
data['biggest_win']=data.groupby('player_id',as_index=False)['prize_usd'].transform('max')
data['win_count']=data.groupby('player_id',as_index=False)['first'].transform('sum')
data['countries_visited']=data.groupby('player_id',as_index=False)['country'].transform('nunique')

data['percent_won']=data['win_count']/data['number_of_events']

data=data[['name','number_of_events','total_prize_money','biggest_win','countries_visited','percent_won']]
#Reduce the data to name, number of events, total prize money, biggest win, percentage won, countries visited, career length
final=data.melt(id_vars='name',var_name='metric',value_name='raw_value')
final=final.drop_duplicates()

final['scaled_value']=final.groupby('metric')['raw_value'].rank(method='average',ascending=True)
final=final.sort_values(['name','metric'])

