import pandas as pd
import xlrd
import re
#Input the data:
xls_sheet=xlrd.open_workbook('data/PD 2021 Wk 7 Shopping List and Ingredients.xlsx')

for index,sheetname in enumerate(xls_sheet.sheet_names()):
    globals()['data%s' %index]=pd.read_excel('data/PD 2021 Wk 7 Shopping List and Ingredients.xlsx',sheet_name=sheetname)


#Prepare the keyword data
# Add an 'E' in front of every E number.
# Stack Animal Ingredients and E Numbers on top of each other.
# Get every ingredient and E number onto separate rows.
data1_clean=[c.lower().strip() for c in data1['Animal Ingredients'][0].split(', ')]+['e'+c.strip() for c in data1['E Numbers'][0].split(',')]

#Append the keywords onto the product list.

data0['ingre']=data0['Ingredients/Allergens'].apply(lambda x:re.sub('\W+',',',x.lower()).split(','))
#Check whether each product contains any non-vegan ingredients.
data0['Contains']=data0['Ingredients/Allergens'].apply(lambda x:', '.join(sorted(list(set(x) & set(data1_clean)))))
# Prepare a final shopping list of vegan products.
# Aggregate the products into vegan and non-vegan.
# Filter out the non-vegan products.
vegan=data0.loc[data0['Contains']=='',['Product','Description']]
non_vegan=data0.loc[data0['Contains']!='',['Product','Description','Contains']]

vegan.to_csv('output/PD 2021 W7 Vegan.csv')
non_vegan.to_csv('output/PD 2021 W7 Non Vegan.csv')