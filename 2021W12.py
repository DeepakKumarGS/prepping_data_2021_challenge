### Prepping data Week 12 2021 ###

##Requirements

# Input the data
# Pivot all of the month fields into a single column (help)
# Rename the fields and ensure that each field has the correct data type
# Filter out the nulls (help)
# Filter our dataset so our Values are referring to Number of Tourists
# Our goal now is to remove all totals and subtotals from our dataset so that only the lowest level of granularity remains. Currently we have Total > Continents > Countries, but we don't have data for all countries in a continent, so it's not as simple as just filtering out the totals and subtotals. Plus in our Continents level of detail, we also have The Middle East and UN passport holders as categories. If you feel confident in your prep skills, this (plus the output) should be enough information to go on, but otherwise read on for a breakdown of the steps we need to take:
# Filter out Total tourist arrivals
# Split our workflow into 2 streams: Continents and Countries
# Hint: the hierarchy field will be useful here
# Split out the Continent and Country names from the relevant fields (help)
# Aggregate our Country stream to the Continent level (help)
# Join the two streams together and work out how many tourists arrivals there are that we don't know the country of (help)
# Add in a Country field with the value "Unknown" (help)
# Union this back to here we had our Country breakdown (help)
# Output the data


import pandas as pd
import re

data=pd.read_csv('data/PD 2021 Wk 12 Tourism Input.csv')


foo = pd.melt(data,id_vars=['id','Series-Measure','Hierarchy-Breakdown','Unit-Detail'],
                var_name='Month',value_name='Number of Tourists')

foo['Month']=foo['Month'].apply(lambda x:pd.to_datetime(x,format='%b-%y').date())
foo=foo[(foo['Unit-Detail']=='Tourists') & (foo['Series-Measure']!='Total tourist arrivals')]

foo['Number of Tourists']=foo['Number of Tourists'].apply(lambda x:pd.to_numeric(x,errors='coerce'))

foo['Breakdown']=foo.apply(lambda x:re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown']).group(1) if re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown'])
                        else re.search('(?:from|-)\s(.*)',x['Series-Measure']).group(1),axis=1)

foo['Country']=foo.apply(lambda x:re.search('from\s(?:the\s)*(.*)',x['Series-Measure']).group(1) if re.search('(?:.*/){3}\s(.*)',x['Hierarchy-Breakdown'])
                        else 'Unknown',axis=1)

foo['Tourists']=foo.apply(lambda x:0 if x['Country']=='Unknown' 
                        else -1*x['Number of Tourists'],axis=1).astype('float32')

foo['temp_sum']=foo['Tourists'].groupby([foo['Breakdown'],foo['Month']]).transform('sum')

foo['Num_Tourist']=foo.apply(lambda x:x['Number of Tourists']+(x['temp_sum'] if x['Country']=='Unknown' else 0),axis=1)

final=foo[['Breakdown','Num_Tourist','Month','Country']].copy()
final.rename({'Num_Tourist':'Number of Tourists'},inplace=True)