### Week 11 2021 Challenge ###
#https://preppindata.blogspot.com/2021/03/2021-week-11-cocktail-profit-margins.html
# Input the dataset 
# Split out the recipes into the different ingredients and their measurements
# Calculate the price in pounds, for the required measurement of each ingredient
# Join the ingredient costs to their relative cocktails
# Find the total cost of each cocktail 
# Include a calculated field for the profit margin i.e. the difference between each cocktail's price and it's overall cost 
# Round all numeric fields to 2 decimal places 
# Output the data


import pandas as pd
import re
import numpy as np

cocktails =pd.read_excel('data/PD 2021 Wk 11 Cocktails Dataset.xlsx',sheet_name='Cocktails')
Sourcing=pd.read_excel('data/PD 2021 Wk 11 Cocktails Dataset.xlsx',sheet_name='Sourcing')
rates=pd.read_excel('data/PD 2021 Wk 11 Cocktails Dataset.xlsx',sheet_name='Conversion Rates')

prep = cocktails.set_index(['Cocktail','Price (£)']).apply(lambda x:x.str.split(";").explode()).reset_index()
prep[['Recipe','ml']]= prep['Recipe (ml)'].str.split(":",expand=True)
prep['ml']=prep['ml'].apply(lambda x:re.sub('ml',"",x))
prep['ml']=prep['ml'].astype('float32')
prep['Recipe']=prep['Recipe'].str.strip()
prep=prep.merge(Sourcing,left_on='Recipe',right_on='Ingredient',how='left')
prep=prep.merge(rates,on='Currency',how='inner')
prep['price_pound']=prep['Price']/prep['Conversion Rate £']
prep['ingre_price']=(prep['ml']*prep['price_pound'])/prep['ml per Bottle']

final=prep.groupby(['Cocktail','Price (£)'])['ingre_price'].sum().reset_index().rename(columns={'ingre_price':'Cost','Price (£)':'Price'})
final['Cost']=np.round(final['Cost'],2)
final['Margin']=final['Price']-final['Cost']

final=final[['Margin','Cost','Cocktail','Price']].reset_index(drop=True)

final.to_csv('output/PD 2021 Wk 11 Output.csv',index=False)