### Prepping Data 2021 Week 18

# Input the data
# Workout the 'Completed Date' by adding on how many days it took to complete each task from the Scheduled Date
# Rename 'Completed In Days from Schedule Date' to 'Days Difference to Schedule'
# Your workflow will likely branch into two at this point:
# 1. Pivot Task to become column headers with the Completed Date as the values in the column
# You will need to remove some data fields to ensure the result of the pivot is a single row for each project, sub-project and owner combination. 
# Calculate the difference between Scope to Build time
# Calculate the difference between Build to Delivery time
# Pivot the Build, Deliver and Scope column to re-create the 'Completed Dates' field and Task field
# You will need to rename these
# 2. You don't need to do anything else to this second flow

# Now you will need to:
# Join Branch 1 and Branch 2 back together 
# Hint: there are 3 join clauses for this join
# Calculate which weekday each task got completed on as we want to know whether these are during the weekend or not for the dashboard
# Clean up the data set to remove any fields that are not required.
# Output as a csv file

import pandas as pd
import numpy as np

data=pd.read_excel('data/PD 2021 Wk 18 Input.xlsx')

data['Completed Date']=pd.to_datetime(data['Scheduled Date'])+pd.to_timedelta(data['Completed In Days from Scheduled Date'],unit='d')

data.rename(columns={'Completed In Days from Scheduled Date':'Days Difference to Schedule'},inplace=True)

task1=data.pivot(index=['Project','Sub-project','Owner'],columns='Task',values='Completed Date').reset_index()

task1['Scope to Build Time']=(task1['Build']-task1['Scope']).dt.days

task1['Build to Delivery Time']=(task1['Deliver']-task1['Build']).dt.days

task1=task1.melt(id_vars=['Project','Sub-project','Owner','Scope to Build Time','Build to Delivery Time'],value_vars=['Build','Deliver','Scope'],value_name='Task Date')

final=data.merge(task1,how='inner',on=['Project','Sub-project','Owner','Task'])

final['Completed Weekday']=final['Completed Date'].dt.day_name()

final=final[['Completed Weekday','Task','Scope to Build Time','Build to Delivery Time','Days Difference to Schedule','Project','Sub-project','Owner','Scheduled Date','Completed Date']]

final.to_csv('output/PD 2021 Wk18 Solution.csv',index=False)