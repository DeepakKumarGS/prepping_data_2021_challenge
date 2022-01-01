# Prepping Data Week 17 2021

# Requirements
# Remove the ‘Totals’ Rows
# Pivot Dates to rows and rename fields 'Date' and 'Hours'
# Split the ‘Name, Age, Area of Work’ field into 3 Fields and Rename
# Remove unnecessary fields
# Remove the row where Dan was on Annual Leave and check the data type of the Hours Field.
# Total up the number of hours spent on each area of work for each date by each employee.

# First we are going to work out the avg number of hours per day worked by each employee
# Calculate the total number of hours worked and days worked per person
# Calculate the avg hours and remove unnecessary fields.

# Now we are going to work out what % of their day (not including Chats) was spend on Client work.
# Filter out Work related to Chats.
# Calculate total number of hours spent working on each area for each employee
# Calculate total number of hours spent working on both areas together for each employee
# Join these totals together
# Calculate the % of total and remove unnecessary fields
# Filter the data to just show Client work
# Join to the table with Avg hours to create your final output



import pandas as pd
import numpy as np
import re

data=pd.read_excel('data/PD 2021 Wk 17 Preppin Data Challenge.xlsx')

foo=pd.melt(data,id_vars=['Name, Age, Area of Work','Project'],value_name='Hours',var_name='Date')

foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Name']=foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Name, Age, Area of Work'].apply(lambda x:re.search('(\w+)(?=,)',x).group(1))

foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Age']=foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Name, Age, Area of Work'].apply(lambda x:re.search('(\d+)(?=:)',x).group(1))

foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Area of Work']=foo.loc[~(foo['Name, Age, Area of Work'].isna()),'Name, Age, Area of Work'].apply(lambda x:re.search('(?<=:)\s+(\w.+)',x).group(1).strip())

#Remove overall Total & Annual Leave Hrs,

foo=foo.loc[~((foo['Name, Age, Area of Work'].isna()) | (foo['Hours']=='Annual Leave')),].copy()

foo['Hours']=foo['Hours'].fillna(0).astype('float')

foo=foo.groupby(['Name','Age','Area of Work','Project','Date'])['Hours'].sum().reset_index()

avg_work_hrs=foo.groupby(['Name']).agg({'Date':'nunique','Hours':'sum'}).reset_index()

avg_work_hrs['Avg Number of Hours worked per day']=avg_work_hrs['Hours']/avg_work_hrs['Date']

client_work=foo.loc[~(foo['Area of Work']=='Chats'),].groupby(['Name','Area of Work'],as_index=False)['Hours'].sum()

total_hrs=client_work.groupby('Name',as_index=False)['Hours'].sum()

client_work=pd.merge(client_work,total_hrs,on='Name').rename(columns={'Hours_y':'Total Hours','Hours_x':'Hours'})

client_work['% of Total']=np.round((client_work['Hours']/client_work['Total Hours'])*100,0)

final=pd.merge(avg_work_hrs,client_work.loc[client_work['Area of Work']=='Client',],on='Name')

final=final[['Name','Area of Work','% of Total','Avg Number of Hours worked per day']].sort_values('% of Total',ascending=False)
