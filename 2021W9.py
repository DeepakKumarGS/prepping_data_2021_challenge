import pandas as pd
import re
import numpy as np
#Input the Customer Information file, split the values and reshape the data so there is a separate ID on each row.
cust_info = pd.read_excel('data/2021W9/Customer Information.xlsx')
area_code=pd.read_excel('data/2021W9/Area Code Lookup.xlsx',dtype='str')
product_code=pd.read_excel('data/2021W9/Product Lookup.xlsx')
#Refr - https://stackoverflow.com/questions/12680754/split-explode-pandas-dataframe-string-entry-to-separate-rows
cust_info = pd.concat([pd.Series(row['IDs'].split(' '))
                for _,row in cust_info.iterrows()]).reset_index(drop=True).to_frame().rename(columns={0:'IDs'})

#The first 6 digits present in each ID is the customers phone number
cust_info['Phone Number']=cust_info['IDs'].apply(lambda x:re.search('(\d{6})(?=,)',x).group(1)) 
#The first 2 digits after the ‘,’ is the last 2 digits of the area code 
cust_info['l_areacode']=cust_info['IDs'].apply(lambda x:re.search('(?<=,)(\d{2})',x).group(1))    
#The letter following this is the first letter of the name of the area that they are calling from
cust_info['f_areaname']=cust_info['IDs'].apply(lambda x:re.search('(?<=\d{2})([A-Z])',x).group(1))     
#The digits after this letter resemble the quantity of products ordered
cust_info['product quantity']=cust_info['IDs'].apply(lambda x:re.search('(?<=[A-Z])(\d+)(?=-)',x).group(1)) 
#The letters after the ‘-‘ are the product ID codes 
cust_info['Product ID']=cust_info['IDs'].apply(lambda x:re.search('(?<=-)([A-Z]+)',x).group(1)) 

#Input the Area Code Lookup Table – find a way to join it to the Customer information file 

#We don’t actually sell products in Clevedon, Fakenham, or Stornoway. Exclude these from our dataset 
area_code=area_code[~area_code['Area'].isin(['Clevedon','Fakenham','Stornoway'])]
#In some cases, the ID field does not provide accurate enough conditions to know where the customer is from. Exclude any phone numbers where the join has produced duplicated records.
area_code['join']=area_code.apply(lambda x:x['Code'][-2:]+x['Area'][0:1],axis=1)
area_code['duplicate_count']=area_code['Area'].groupby(area_code['join']).transform('count')

cust_info['join']=cust_info['l_areacode']+cust_info['f_areaname']
final =pd.merge(cust_info[cust_info['product quantity'].astype('int')>0],area_code[area_code['duplicate_count']==1],on='join')
#Remove any unwanted fields created from the join.  
final.drop(['l_areacode','f_areaname','join','duplicate_count','Code','IDs','Phone Number'],axis=1,inplace=True)
#Join this dataset to our product lookup table.
final=pd.merge(final,product_code,on='Product ID')
#For each area, and product, find the total sales values, rounded to zero decimal places
final['Price']=final['Price'].apply(lambda x:float(x[1:]))
final['Sales']=final['Price']*final['product quantity'].astype('int')
final=final.groupby(['Area','Product Name'],as_index=False)['Sales'].sum()
final['Sales']=np.round(final['Sales']).astype('int')
#Rank how well each product sold in each area.
final['Rank']=final['Sales'].groupby(final['Area']).rank(ascending=False).astype('int')
final['Area Sales']=final['Sales'].groupby(final['Area']).transform('sum')
#For each area, work out the percent of total that each different product contributes to the overall revenue of that Area, rounded to 2 decimal places
final['% of Total - Product']=final.apply(lambda x:round((x['Sales']/x['Area Sales'])*100,2),axis=1)
final=final.sort_values('Area Sales',ascending=False)
final=final[['Rank','Area','Product Name','Sales','% of Total - Product']]

#Output the data 
final.to_csv('output/PD 2021 W9 Output.csv',index=False)