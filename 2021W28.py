# Prepping Data 2021 Week 28

from typing import AsyncGenerator
import pandas as pd
import re
import numpy as np

world_cup=pd.read_excel('data/PD 2021 Wk28 InternationalPenalties.xlsx',sheet_name='WorldCup')
euros=pd.read_excel('data/PD 2021 Wk28 InternationalPenalties.xlsx',sheet_name='Euros')

world_cup['penality']='WorldCup'
world_cup['Date']=pd.to_datetime(world_cup['Date'],format='%Y-%m-%d')

euros['penality']='Euro'
euros['Date']=pd.to_datetime(euros['Date'],format='%Y-%m-%d')

full=pd.concat([world_cup,euros])

full['Winner']=full['Winner'].str.strip()
full['Loser']=full['Loser'].str.strip()

full=full.replace({'Winner':{'West Germany':'Germany'},'Loser':{'West Germany':'Germany'}})

full['Winning Team Penality']=full['Winning team Taker'].apply(lambda x:1 if re.search('(scored)',str(x)) else 0)
full['Losing Team Penality']=full['Losing team Taker'].apply(lambda x:1 if re.search('(scored)',str(x)) else 0)

full['Winner Total Penalities']=full['Winning team Taker'].apply(lambda x:0 if pd.isna(x) else 1)
full['Loser Total Penalities']=full['Losing team Taker'].apply(lambda x:0 if pd.isna(x) else 1)

out1=full[['penality','No.','Winner','Loser']].drop_duplicates().copy()
out1=pd.melt(out1,id_vars=['penality','No.'],value_name='Teams',var_name='Win Lost')
out1['Shootouts']=out1['Win Lost'].apply(lambda x:1 if x=='Winner' else 0)
out1['Total Shootouts']=1
out1=out1.groupby(['Teams'],as_index=False).agg({'Shootouts':'sum','Total Shootouts':'sum'})
out1=out1[out1['Shootouts']>0]
out1['Shootout Win %']=np.round((out1['Shootouts']/out1['Total Shootouts'])*100)
out1['Rank']=out1['Shootout Win %'].rank(method='dense',ascending=False).astype(int)
out1=out1[['Rank','Shootout Win %','Total Shootouts','Shootouts','Teams']].sort_values(['Rank','Shootout Win %'],ascending=[True,False])

out2=full[['Winner','Loser','Winning Team Penality','Winner Total Penalities','Losing Team Penality','Loser Total Penalities']].copy()
out2=pd.melt(out2,id_vars=[c for c in out2.columns if re.search('\s\w',c)],value_name='Team',var_name='Win Lose')
out2['Penalities Scored']=out2.apply(lambda x:x['Winning Team Penality'] if x['Win Lose']=='Winner' else x['Losing Team Penality'],axis=1)
out2['Total Penalities']=out2.apply(lambda x:x['Winner Total Penalities'] if x['Win Lose']=='Winner' else x['Loser Total Penalities'],axis=1)
out2=out2.groupby(['Team'],as_index=False).agg({'Penalities Scored':'sum','Total Penalities':'sum'})
out2['Penalities Missed']=out2['Total Penalities']-out2['Penalities Scored']
out2['% Penalities Scored']=np.round((out2['Penalities Scored']/out2['Total Penalities'])*100)
out2['Penalities Scored % rank']=out2['% Penalities Scored'].rank(method='dense',ascending=False).astype(int)
out2=out2[['Penalities Scored % rank','% Penalities Scored','Penalities Missed','Penalities Scored','Team']].sort_values(['Penalities Scored % rank','% Penalities Scored'],ascending=[True,False])



