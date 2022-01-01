### Prepping Data 2021 Week 16

# Input the data
# Calculate the Total Points for each team. The points are as follows: 
# Win - 3 Points
# Draw - 1 Point
# Lose - 0 Points
# Calculate the goal difference for each team. Goal difference is the difference between goals scored and goals conceded. 
# Calculate the current rank/position of each team. This is based on Total Points (high to low) and in a case of a tie then Goal Difference (high to low).
# The current league table is our first output.

# Assuming that the 'Big 6' didn't play any games this season, recalculate the league table.
# After removing the 6 clubs, how has the position changed for the remaining clubs?
# The updated league table is the second output.

import pandas as pd
import numpy as np

data=pd.read_csv('data/PD 2021 Wk16 PL Fixtures.csv')

data=data.loc[~data['Result'].isna(),]

def get_pts_tbl(df):


    df[['Home Team Goal','Away Team Goal']]=df['Result'].str.split('-',expand=True).astype('int32')

    df.loc[:,'Home Team Pts']=np.select(
        [df['Home Team Goal'] > df['Away Team Goal'],
        df['Home Team Goal']< df['Away Team Goal'],
        df['Home Team Goal']==df['Away Team Goal']],
        [3,
        0,
        1],
        default='Unknown'
    )

    df.loc[:,'Away Team Pts']=np.select(
        [df['Away Team Goal'] > df['Home Team Goal'],
        df['Away Team Goal']< df['Home Team Goal'],
        df['Away Team Goal']==df['Home Team Goal']],
        [3,
        0,
        1],
        default='Unknown'
    )

    df[['Home Team Pts','Away Team Pts']]=df[['Home Team Pts','Away Team Pts']].astype('int32')

    df.loc[:,'Home Goal Difference']=df['Home Team Goal']-df['Away Team Goal']

    df.loc[:,'Away Goal Difference']=df['Away Team Goal']-df['Home Team Goal']

    ## Home Team & Away Team :
    cols=['Date','Team','Team Goal','Team Pts','Goal Diff']
    home_team=df[['Date','Home Team','Home Team Goal','Home Team Pts','Home Goal Difference']]
    home_team.columns=cols
    away_team=df[['Date','Away Team','Away Team Goal','Away Team Pts','Away Goal Difference']]
    away_team.columns=cols
    foo=pd.concat([home_team,away_team])

    return foo.copy()

league=get_pts_tbl(data)
league.loc[:,'Total Games Played']=1
orig_league=league.groupby('Team',as_index=False).agg({'Total Games Played':'sum','Team Pts':'sum','Goal Diff':'sum'})
orig_league.loc[:,'Position']=orig_league[['Team Pts','Goal Diff']].apply(tuple,axis=1).rank(method='dense',ascending=False).astype('int32')
orig_league=orig_league.sort_values('Position')

big6=['Arsenal','Chelsea','Liverpool','Man Utd','Man City','Spurs']

super_league=data.loc[~(data['Home Team'].isin(big6) | data['Away Team'].isin(big6)),]
super_league=get_pts_tbl(super_league)
super_league.loc[:,'Total Games Played']=1
super_league=super_league.groupby('Team',as_index=False).agg({'Total Games Played':'sum','Team Pts':'sum','Goal Diff':'sum'})
super_league.loc[:,'Super League Position']=super_league[['Team Pts','Goal Diff']].apply(tuple,axis=1).rank(method='dense',ascending=False).astype('int32')
super_league=super_league.sort_values('Super League Position').reset_index(drop=True)

super_league=pd.merge(super_league,orig_league[['Team','Position']].rename(columns={'Position':'Original Position'}),on='Team')

super_league['Position Change']=super_league['Original Position']-super_league['Super League Position']

super_league.rename(columns={'Super League Position':'Position','Team Pts':'Total Points','Goal Diff':'Goal Difference'},inplace=True)

super_league=super_league[['Position Change','Position','Team','Total Games Played','Total Points','Goal Difference']]