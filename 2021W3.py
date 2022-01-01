import pandas as pd
import xlrd 

xls_file=xlrd.open_workbook('data/PD 2021 Wk 3 Input.xlsx',on_demand=True)
#Input the data source by pulling together all the tables
#Create a Store column from the data
for index,sheet in enumerate(xls_file.sheet_names()):
    globals()['data%s' %index]=pd.read_excel('data/PD 2021 Wk 3 Input.xlsx',sheet_name=sheet)
    globals()['data%s' %index]['Store']=sheet

data=pd.concat([data0,data1,data2,data3,data4],axis=0).reset_index(drop=True)

#Pivot 'New' columns and 'Existing' columns 

data_pivot=pd.melt(data,id_vars=['Store','Date'],var_name='customer_model')

#Split the former column headers to form:
# Customer Type
# Product

data_pivot[['Customer','Model']]=data_pivot['customer_model'].str.split('-',expand=True).apply(lambda x:x.str.strip())
#Remove any unnecessary data fields

data_pivot.drop('customer_model',axis=1,inplace=True)
#Rename the measure created by the Pivot as 'Products Sold'

data_pivot.rename(columns={'value':'Products Sold','Model':'Product','Customer':'Customer Type'},inplace=True)

#Turn Date into Quarter
data_pivot['Date']=pd.to_datetime(data_pivot['Date'])
data_pivot['Quarter']=data_pivot['Date'].dt.quarter

#Aggregate to form two separate outputs of the number of products sold by
#Product, Quarter
#Store, Customer Type, Product
result_a=data_pivot.groupby(['Product','Quarter'])['Products Sold'].sum().reset_index()
result_b=data_pivot.groupby(['Store','Customer Type','Product'])['Products Sold'].sum().reset_index()

#Output each data set as a csv file
result_a.to_csv('output/PD 2021 W3 Output 1.csv',index=False)
result_b.to_csv('output/PD 2021 W3 Output 2.csv',index=False)