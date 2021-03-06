# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:53:37 2018

@author: mm
"""

# Read datas
customers=pd.read_csv('customers.csv')
customers=customers.drop(['Unnamed: 0'],axis=1)

coupon=pd.read_csv('coupon2.csv',index_col=['id'])# id as index

service=pd.read_csv('service2.csv',index_col=['id'])# id as index

target=pd.read_csv('target.csv')
target['id']=target['id'].astype(int)
target['gold']=target['gold'].astype(int)
target=target.drop(['Unnamed: 0'],axis=1)
target=target.set_index(['id'])# id as index

spend=pd.read_csv('spend2.csv',index_col=['id'])# id as index

demo_real=pd.read_csv('demo_real.csv')
demo_real=demo_real.drop(['Unnamed: 0'],axis=1)

# merge tables
model_table=target.merge(coupon, how='left', left_index=True, right_index=True)
model_table=model_table.merge(service, how='left', left_index=True, right_index=True)
model_table=model_table.merge(spend, how='left', left_index=True, right_index=True)

customers_demo_real=pd.merge(customers,demo_real, how='left', left_on='postcode', right_on='POSTCODE')
customers_demo_real=customers_demo_real.set_index(['id'])

model_table=model_table.merge(customers_demo_real, how='left', left_index=True, right_index=True)

####
# Modify Model Table
#create dummy variables for object variables:
model_table.drop(['internet_day','birth','postcode','POSTCODE','reg_day'],axis=1,inplace=True)
#dummy_cols=model_table.select_dtypes(include=['object']).columns.tolist() # object variables
#
##create dummy variables for object variables:
#dummy_table=pd.get_dummies(model_table['sex'],prefix='sex') # Dummy table initialization
#dummy_cols.remove('sex')
#
#for i in dummy_cols:
#    dummy=pd.get_dummies(model_table.loc[:,i],prefix=i)
#    dummy_table=dummy_table.merge(dummy, how='inner', left_index=True, right_index=True)
#
#model_table.drop(dummy_cols+['sex'],axis=1,inplace=True) 
#model_table=model_table.merge(dummy_table, how='inner', left_index=True, right_index=True) 

model_table.to_csv('model_table.csv')