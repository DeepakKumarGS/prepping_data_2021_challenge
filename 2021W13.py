### Prepping Data W13 2021 ###

# Input all the files
# Remove all goalkeepers from the data set
# Remove all records where appearances = 0	
# In this challenge we are interested in the goals scored from open play
# Create a new “Open Play Goals” field (the goals scored from open play is the number of goals scored that weren’t penalties or freekicks)
# Note some players will have scored free kicks or penalties with their left or right foot
# Be careful how Prep handles null fields! (have a look at those penalty and free kick fields) 
# Rename the original Goals scored field to Total Goals Scored
# Calculate the totals for each of the key metrics across the whole time period for each player, (be careful not to lose their position)
# Create an open play goals per appearance field across the whole time period
# Rank the players for the amount of open play goals scored across the whole time period, we are only interested in the top 20 (including those that are tied for position) – Output 1
# Rank the players for the amount of open play goals scored across the whole time period by position, we are only interested in the top 20 (including those that are tied for position) – Output 2
# Output the data – in your solution on twitter / the forums, state the name of the player who was the only non-forward to make it into the overall top 20 for open play goals scored

import pandas as pd
import numpy as np
import glob
#Input the file
files=glob.glob('data/2021W13/*.csv')

dfs=[]
for f in files:
    df=pd.read_csv(f,header=0,index_col=None)
    dfs.append(df)

game=pd.concat(dfs,axis=0,ignore_index=True)

game =game[~(game['Position']=='Goalkeeper')]
game=game[~(game['Appearances']==0)]
game=game.fillna(0)

game['Open Play Goals']=game['Goals']-(game['Penalties scored']+game['Freekicks scored'])

foo=game.groupby(['Name','Position'])['Goals','Open Play Goals','Goals with right foot','Goals with left foot','Appearances','Headed goals'].sum().reset_index().rename({'Goals':'Total Goals'},axis=1)

foo['Open Play Goals/Game']=foo['Open Play Goals']/foo['Appearances']

foo['Rank']=foo['Open Play Goals'].rank(ascending=False,method='min').astype(int)

final1=foo.loc[foo['Rank']<=20].sort_values('Rank',ascending=True)

final1=final1[['Open Play Goals','Goals with right foot','Goals with left foot','Position','Appearances','Rank','Total Goals','Open Play Goals/Game','Headed goals','Name']]

final1.loc[final1['Position']!='Forward']['Name']

foo['Rank by Position']=foo['Open Play Goals'].groupby(foo['Position']).rank(ascending=False,method='min').astype(int)

final2=foo.loc[foo['Rank by Position']<=20]

final2=final2.sort_values('Rank by Position',ascending=True).reset_index(drop=True)


final2=final2[['Rank by Position','Open Play Goals','Goals with right foot','Goals with left foot','Position','Appearances','Total Goals','Open Play Goals/Game','Headed goals','Name']]