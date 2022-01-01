# Prepping Data 2021 Week 46
import pandas as pd

#Read sales data,
q1_sale=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Sales Q1')
q2_sale=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Sales Q2')
q3_sale=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Sales Q3')
q4_sale=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Sales Q4')

edition=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Edition')
publisher=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Publisher')
author=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Author')
book=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Book')
info=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Info')
award=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Award')
checkouts=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Checkouts')
ratings=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Ratings')
series=pd.read_excel('data/PD 2021 Wk 46 Bookshop.xlsx',sheet_name='Series')

#Union all the Sales data together to form one row per item in a sale
sales =pd.concat([q1_sale,q2_sale,q3_sale,q4_sale],axis=0)
#Join all other data sets in the workbook on to this data
#Never let the number of rows change
#You may need to disregard incomplete records or summarise useful data into a metric instead of including all the detail

award=award.groupby('Title',as_index=False)['Award Name'].count().rename(columns={'Award Name':'Number of Awards Won (avg only)'})
checkouts=checkouts.groupby('BookID',as_index=False).agg({'CheckoutMonth':'nunique','Number of Checkouts':'sum'}).rename(columns={'CheckoutMonth':'Number of Months Checked Out','Number of Checkouts':'Total Checkouts'})
ratings=ratings.groupby('BookID',as_index=False).agg({'Rating':'mean','ReviewerID':'count','ReviewID':'count'}).rename(columns={'Rating':'Average Rating','ReviewerID':'Number of Reviewers','ReviewID':'Number of Reviews'})

info['BookID']=info['BookID1'].astype('str')+info['BookID2'].astype('str')
info.drop(['BookID1','BookID2'],axis=1,inplace=True)

sales=pd.merge(sales,edition,on='ISBN') # Join editor
sales=pd.merge(sales,publisher,on='PubID') # Join publisher
sales=pd.merge(sales,book,on='BookID') # join Book
sales=pd.merge(sales,author,on='AuthID') # join  author


sales=pd.merge(sales,info,on='BookID') # join info
sales=pd.merge(sales,award,on='Title',how='left')# join award
sales=pd.merge(sales,checkouts,on='BookID') # join checkouts
sales=pd.merge(sales,ratings,on='BookID') # join ratings
sales=pd.merge(sales,series,on='SeriesID',how='left') # join series











