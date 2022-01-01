## Prepping Data 2021 Week 19

# Input the data
# There are lots of different ways you can do this challenge so rather than a step-by-step set of requirements, feel free to create each of these data fields in whatever order you like:
# 'Week' with the word week and week number together 'Week x' 
# 'Project' with the full project name
# 'Sub-Project' with the full sub-project name
# 'Task' with the full type of task
# 'Name' with the owner of the task's full name (Week 18's output can help you check these if needed) 
# 'Days Noted' some fields have comments that say how many days tasks might take. This field should note the number of days mentioned if said in the comment otherwise leave as a null. 
# 'Detail' the description from the system output with the project details in the [ ] 
# Output the file

import pandas as pd
import re

proj_schedule=pd.read_excel("data/PD 2021 Week 19 Input.xlsx",sheet_name='Project Schedule Updates')
proj_lookup=pd.read_excel("data/PD 2021 Week 19 Input.xlsx",sheet_name='Project Lookup Table')
sub_proj_lookup=pd.read_excel("data/PD 2021 Week 19 Input.xlsx",sheet_name='Sub-Project Lookup Table')
task_lookup=pd.read_excel("data/PD 2021 Week 19 Input.xlsx",sheet_name='Task Lookup Table')
owner_lookup=pd.read_excel("data/PD 2021 Week 19 Input.xlsx",sheet_name='Owner Lookup Table')

owner_lookup['Abbreviation']=owner_lookup['Abbreviation'].str.lower()

project=pd.concat([pd.Series(rows['Week'],rows['Commentary'].split('[')) for _,rows in proj_schedule.iterrows()]).reset_index().rename(columns={'index':'Details',0:'Week'})

def lookup(data,lookup_table,column):
    data=data.merge(lookup_table,how='left',on=column)
    data.drop(column,axis=1,inplace=True)
    return data

project['Details']=project['Details'].str.strip()
project=project.loc[~(project['Details']==''),]
##Get project code,
project.loc[:,'Project Code']=project.loc[:,'Details'].apply(lambda x:re.search('(\w+)(?=/)',x).group(1))
#Get sub-project code,
project.loc[:,'Sub-Project Code']=project.loc[:,'Details'].apply(lambda x:re.search('(?<=/)(\w+)',x).group(1)).str.lower()
## Convert ops to op,
project.loc[project['Sub-Project Code']=='ops','Sub-Project Code']='op'
##Get task code,
project.loc[:,'Task Code']=project.loc[:,'Details'].apply(lambda x:re.search('(?<=-)(\w+)',x).group(1))
##Get abbreviation,
project.loc[:,'Abbreviation']=project.loc[:,'Details'].apply(lambda x:re.search('(?<=\s)(\w+)(?=.$)',x).group(1))
##Remove block between []
project.loc[:,'Details']=project.loc[:,'Details'].apply(lambda x:re.sub('(.*]\s)','',x))

bar=lookup(project,proj_lookup,'Project Code') ## Change project code abbr.
bar=lookup(bar,sub_proj_lookup,'Sub-Project Code') ## 
bar=lookup(bar,task_lookup,'Task Code') 
final=lookup(bar,owner_lookup,'Abbreviation') 
## Gets days noted,
final.loc[:,'Days Noted']=final.loc[:,'Details'].apply(lambda x:re.search('(\d+)',x).group(1) if re.search('(\d+)',x) else '')

final['Week']='Week '+final['Week'].astype('str')




