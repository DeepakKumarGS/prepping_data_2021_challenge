# Prepping Data 2021 Week 49

import pandas as pd
import numpy as np

data=pd.read_csv('data/PD 2021 Wk 49 Input - Input.csv')

data['Date']=pd.to_datetime(data['Date'],format='%d/%m/%Y')

data['Report Year']=data['Date'].dt.year
#Create the Employment Range field which captures the employees full tenure at the company in the MMM yyyy to MMM yyyy format. 

data['Min Date']=data.groupby('Name')['Date'].transform('min').dt.strftime('%b %Y')

data['Max Date']=data.groupby('Name')['Date'].transform('max').dt.strftime('%b %Y')

data['Employment Range']=data['Min Date'] + ' to ' + data['Max Date']

data['Tenure by End of Reporting Year']=data.sort_values('Date').groupby('Name').cumcount()+1

data['Salary Paid']=data['Annual Salary']/12

# Determine the bonus payments the person will have received each year
# It's 5% of their sales total

data['Yearly Bonus']=0.05*data['Sales']

# Work out for each year employed per person:
# Number of months they worked
# Their salary they will have received 
# Their sales total for the year

data=data.groupby(['Name','Report Year'],as_index=False).agg({'Employment Range':'first','Tenure by End of Reporting Year':'max','Salary Paid':'sum','Yearly Bonus':'sum'})
#Round Salary Paid and Yearly Bonus to two decimal places 
data['Salary Paid']=np.round(data['Salary Paid'],2)

data['Yearly Bonus']=np.round(data['Yearly Bonus'],2)

#Add Salary Paid and Yearly Bonus together to form Total Paid

data['Total Paid']=data['Salary Paid']+data['Yearly Bonus']




