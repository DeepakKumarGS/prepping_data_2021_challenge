import pandas as pd
import xlrd
#Input the file 
xls_file = xlrd.open_workbook('data/PD 2021 Wk 4 Input.xlsx')

for index,sheetname in enumerate(xls_file.sheet_names()):
    globals()['data%s' %index]=pd.read_excel('data/PD 2021 Wk 4 Input.xlsx',sheet_name=sheetname)
    globals()['data%s' %index]['Store_name']=sheetname

#Union the Stores data together 
data=pd.concat([data0,data1,data2,data3,data4],axis=0)

data5.drop('Store_name',axis=1,inplace=True)

#Pivot the product columns
data_pivot=pd.melt(data,id_vars=['Date','Store_name'],var_name='customer_type_product')

# Split the 'Customer Type - Product' field to create:
# Customer Type
# Product
# Also rename the Values column resulting from you pivot as 'Products Sold'

data_pivot[['Customer Type','Product']]=data_pivot['customer_type_product'].str.split('-',expand=True).apply(lambda x:x.str.strip())

data_pivot.drop('customer_type_product',axis=1,inplace=True)

data_pivot.rename(columns={'value':'Products Sold'},inplace=True)

#Turn the date into a 'Quarter' number 
data_pivot['Date']=pd.to_datetime(data_pivot['Date'],format='%Y-%m-%d')
data_pivot['Quarter']=data_pivot['Date'].dt.quarter

#Sum up the products sold by Store and Quarter 
products_sold=data_pivot.groupby(['Store_name','Quarter'])['Products Sold'].sum().reset_index()
products_sold.rename(columns={'Store_name':'Store'},inplace=True)

#Add the Targets data 
#Join the Targets data with the aggregated Stores data 
data_join = products_sold.merge(data5,how='left')

#Calculate the Variance between each Store's Quarterly actual sales and the target. Call this field 'Variance to Target'
data_join['Variance to Target']=data_join['Products Sold']-data_join['Target']

#Rank the Store's based on the Variance to Target in each quarter 
#The greater the variance the better the rank
data_join['Rank']=data_join.groupby('Quarter')['Variance to Target'].rank(ascending=False).astype(int)
#Output the data
result_a=data_join.sort_values(by=['Quarter','Rank'])[['Quarter','Rank','Store','Products Sold','Target','Variance to Target']]
result_a.to_csv('output/PD 2021 Wk 4 Output.csv')
