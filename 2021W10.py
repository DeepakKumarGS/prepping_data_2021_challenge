import pandas as pd
import numpy as np
#Input the data
pokemon=pd.read_excel('data/PD 2021 Wk 10 Pokemon Input.xlsx',sheet_name='Pokemon')
evolution=pd.read_excel('data/PD 2021 Wk 10 Pokemon Input.xlsx',sheet_name='Evolution').drop_duplicates()

#Filter number till 386,Remove names starting with Mega,

pokemon['#']=pokemon['#'].astype('float32')
pokemon=pokemon.loc[pokemon['#']<=386,]
pokemon=pokemon[~(pokemon['Name'].str.startswith('Mega'))]
#remove type,
pokemon.drop('Type',axis=1,inplace=True)
pokemon.drop_duplicates(inplace=True)

evolution=evolution[evolution['Evolving to'].isin(pokemon['Name']) &
                    evolution['Evolving from'].isin(pokemon['Name'])]

def get_evo_grp(name):
    if name not in evo_dict.keys() or name==evo_dict[name]:
        return name
    else:
        return get_evo_grp(evo_dict[name])

evo_dict=dict(zip(evolution['Evolving to'],evolution['Evolving from']))

final=pd.merge(pokemon,evolution,how='left',left_on='Name',right_on='Evolving from')
final['Evolving from']=[evo_dict[k] if k in evo_dict.keys() else np.nan for k in final['Name']]

final['Evolution Group']=final['Name'].apply(get_evo_grp)

final['First Evolution']=[np.nan if (n==g)|(g==f) else g
                                for n,g,f in zip(final['Name'],final['Evolution Group'],final['Evolving from'])]

final.drop_duplicates(inplace=True)

final=final[['Evolution Group','#','Name','Total','HP','Attack','Defense',
            'Special Attack','Special Defense','Speed','Evolving from',
            'Evolving to','Level','Condition','Evolution Type',
            'First Evolution']]


