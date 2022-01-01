### Prepping Data Week 15 ### 

# Input the data

# Modify the structure of the Menu table so we can have one column for the Type (pizza, pasta, house plate), the name of the plate, ID, and Price (hint)

# Modify the structure of the Orders table to have each item ID in a different row (hint)

# Join both tables (hint)

# On Monday's we offer a 50% discount on all items. Recalculate the prices to reflect this

# For Output 1, we want to calculate the total money for each day of the week (hint)

# For Output 2, we want to reward the customer who has made the most orders for their loyalty. Work out which customer has ordered the most single items. 

import pandas as pd

menu=pd.read_excel('data/PD 2021 Wk 15 Menu and Orders.xlsx',sheet_name='MENU')
order=pd.read_excel('data/PD 2021 Wk 15 Menu and Orders.xlsx',sheet_name='Order')

col_names=['Plate_Name','Price','ID','Type']

pizza = menu.iloc[:,0:3]
pizza['Type']='Pizza'
pizza.columns=col_names
pasta=menu.iloc[:,3:6].dropna()
pasta['Type']='Pasta'
pasta.columns=col_names
house_plate=menu.iloc[:,6:9].dropna()
house_plate['Type']='House Plate'
house_plate.columns=col_names

menus=pd.concat([pizza,pasta,house_plate],ignore_index=True)
menus['ID']=menus['ID'].astype('int')
order['Order']=order['Order'].astype('str')

order['Order Date']=pd.to_datetime(order['Order Date'],format='%Y-%d-%m')

orders=order.set_index(['Customer Name','Order Date']).apply(lambda x:x.str.split('-').explode()).reset_index()
orders['Order']=orders['Order'].astype('int')
restaurant=menus.merge(orders,how='left',
                        right_on='Order',
                        left_on='ID')
restaurant['Order Day']=restaurant['Order Date'].dt.weekday

week_map={6:'Sunday',
         0:'Monday',
         1:'Tuesday',
         2:'Wednesday',
         3:'Thursday',
         4:'Friday',
         5:'Saturday'}

restaurant['Order Day']=restaurant['Order Day'].map(week_map)

restaurant.loc[restaurant['Order Day']=='Monday','Price']=(0.5*restaurant.loc[restaurant['Order Day']=='Monday','Price'])

final_1=restaurant.groupby('Order Day')['Price'].sum().sort_values(ascending=False).reset_index()

final_2=restaurant.groupby('Customer Name')['Plate_Name'].nunique().sort_values(ascending=False).reset_index().rename(columns={'Plate_Name':'Count Items'})

final_2=final_2.head(1)