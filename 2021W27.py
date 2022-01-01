# Prepping Data 2021 Week 27

##Reference:Arsene Xie (@ArseneXie)

import pandas as pd
import random
random.seed(42)
teams=pd.read_excel('data/PD 2021 Wk 27 Input.xlsx',sheet_name='Teams')
seeding=pd.read_excel('data/PD 2021 Wk 27 Input.xlsx',sheet_name='Seeding')

team=teams['Seed'].tolist()
temp=[]

#random.choices(team,weights=tuple(list(seeding[1])),k=1)[0]

for rnd in range(1,5):
    print(seeding[rnd])
    pick=random.choices(team,weights=tuple(list(seeding[rnd])),k=1)[0]
    print(rnd,pick)
    df=teams[teams['Seed']==pick].copy()
    df['Actual Pick']=rnd
    temp.append(df)
    team.remove(pick)
    print(f'Team {team}')
    seeding=seeding[seeding['Seed']!=pick].copy()
    print(f'seeding:{seeding}')

picked=pd.concat(temp)

remain=teams[teams['Seed'].isin(team)].copy()
remain['Actual Pick']=remain['Seed'].rank(ascending=True).astype(int)+rnd

final=pd.concat([picked,remain])[['Actual Pick','Seed','Team']].rename(columns={'Seed':'Original'})


