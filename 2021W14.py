### Prepping Data 2021 Week 14 ###

# Input the Data
# Assign a label for where each seat is located. (Hint)
# They are assigned as follows:
# A & F - Window Seats
# B & E - Middle Seats
# C & D - Aisle Seats 
# Combine the Seat List and Passenger List tables. (Hint)

# Parse the Flight Details so that they are in separate fields (Hint) 

# Calculate the time of day for each flight. (Hint)
# They are assigned as follows: 
# Morning - Before 12:00 
# Afternoon - Between 12:00 - 18:00
# Evening - After 18:00

# Join the Flight Details & Plane Details to the Passenger & Seat tables. We should be able to identify what rows are Business or Economy Class for each flight. (Hint)

# Answer the following questions: 
# What time of day were the most purchases made? We want to take a look at the average for the flights within each time period. 
# What seat position had the highest purchase amount? Is the aisle seat the highest earner because it's closest to the trolley?
# As Business Class purchases are free, how much is this costing us? 
# Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you combine all of the outputs into a single Excel workbook, with a different sheet for each output?


import pandas as pd
import re
import numpy as np

passenger_list=pd.read_excel('data/PD 2021 Wk14 - Input.xlsx',sheet_name='Passenger List')
seat_list=pd.read_excel('data/PD 2021 Wk14 - Input.xlsx',sheet_name='SeatList')
flightdetails=pd.read_excel('data/PD 2021 Wk14 - Input.xlsx',sheet_name='FlightDetails')
planedetails=pd.read_excel('data/PD 2021 Wk14 - Input.xlsx',sheet_name='PlaneDetails')

passenger_list=passenger_list.loc[:,~passenger_list.columns.str.contains('^Unnamed')]
seat_names = {'A':'Window Seat',
                'F':'Window Seat',
                'B':'Middle Seat',
                'E':'Middle Seat',
                'C':'Aisle Seat',
                'D':'Aisle Seat',
                'Row':'Row'}

seat_list.columns=seat_list.columns.map(seat_names)

seats=pd.melt(seat_list,id_vars=['Row'],var_name='Seat Position')

manifest=pd.merge(passenger_list,seats,left_on='passenger_number',right_on='value',how='inner')
manifest.drop(['value'],axis=1,inplace=True)

flightdetails['[FlightID|DepAir|ArrAir|DepDate|DepTime]']=flightdetails['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].apply(lambda x:re.sub('(\[|\])','',x))

flightdetails=flightdetails['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].str.split('|',expand=True)

flightdetails.columns=['FlightID','DepAir','ArrAir','DepDate','DepTime']
flightdetails['FlightID']=flightdetails['FlightID'].astype('int32')
flightdetails['DepHour']=pd.to_datetime(flightdetails['DepTime'],format='%H:%M:%S').dt.hour

morning=(flightdetails['DepHour']<12)
afternoon=((flightdetails['DepHour']>=12) & (flightdetails['DepHour']<18))
evening=(flightdetails['DepHour']>=18)

flightdetails.loc[morning,'Depart Time of Day']='Morning'
flightdetails.loc[afternoon,'Depart Time of Day']='Afternoon'
flightdetails.loc[evening,'Depart Time of Day']='Evening'
planedetails['BC']=planedetails['Business Class'].apply(lambda x:re.search('-(\d+)',x).group(1)).astype('int')

manifest=pd.merge(manifest,flightdetails,how='inner',
                left_on='flight_number',
                right_on='FlightID')
manifest=pd.merge(manifest,planedetails,how='inner',
                left_on='flight_number',
                right_on='FlightNo.')
manifest['Class']=np.where(manifest['Row']<=manifest['BC'],'Business','Economy')

final1=manifest.loc[manifest['Class']=='Economy'].groupby(['flight_number','Depart Time of Day'])['purchase_amount'].sum().reset_index()
final1=final1.groupby('Depart Time of Day')['purchase_amount'].mean().reset_index().sort_values('purchase_amount',ascending=False)
final1['Rank']=final1['purchase_amount'].rank(ascending=False).astype('int')
final1.rename(columns={'purchase_amount':'Purchase Amount'},inplace=True)

final2=manifest.loc[manifest['Class']=='Economy'].groupby('Seat Position')['purchase_amount'].sum().reset_index().sort_values('purchase_amount',ascending=False)
final2['Rank']=final2['purchase_amount'].rank(ascending=False).astype('int')
final2.rename(columns={'purchase_amount':'Purchase Amount'},inplace=True)

final3=manifest.groupby('Class')['purchase_amount'].sum().reset_index().sort_values('purchase_amount',ascending=False)
final3['Rank']=final3['purchase_amount'].rank(ascending=False).astype('int')
final3.rename(columns={'purchase_amount':'Purchase Amount'},inplace=True)


