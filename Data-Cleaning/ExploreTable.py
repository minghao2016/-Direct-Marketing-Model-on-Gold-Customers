# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:46:35 2018

@author: mm
"""

def explore(df):

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numericdf = df.select_dtypes(include=numerics)
    if 'id' in df.columns:
        numericdf=numericdf.drop(['id'],axis=1)
    rownum=df.shape[0]
    missnum=numericdf.isnull().sum()
    explorenumeric={'var_name':numericdf.columns.tolist(),
    'mean':numericdf.mean(axis=0).tolist(),
    'median':numericdf.median(axis=0).tolist(),
    'max': numericdf.max(axis=0).tolist(), 
    'min': numericdf.min(axis=0).tolist(),
    'miss_num':missnum.tolist(),
    'non_miss_num':[rownum-x for x in missnum.tolist()],
    'miss_per': (missnum/rownum).tolist(), 
    'replace_code':['if '+str(numericdf.columns[i])+'=Nan then '+str(numericdf.columns[i])+'=mean('+str(numericdf.columns[i])+')' if missnum[i]/rownum<0.3 else '' for i in range(numericdf.shape[1]) ],
    'drop':((missnum/rownum)>0.3).tolist(), 
    'miss_code':['df[ind_'+str(numericdf.columns[i])+']='+str(numericdf.columns[i])+'.isnull()*1' if 0.05<missnum[i]/rownum<0.8 else '' for i in range(numericdf.shape[1])],
    'miss_ind_name':['ind_'+str(numericdf.columns[i]) if 0.05<missnum[i]/rownum<0.8 else '' for i in range(numericdf.shape[1]) ],
    'rep':((missnum/rownum)<=0.3).tolist(),
    'miss':((missnum/rownum)<0.8).tolist()}                         
    explorenumerictable=pd.DataFrame(explorenumeric)
    explorenumerictable=explorenumerictable.set_index('var_name')
    return explorenumerictable

# build explore table for customers:                        
explorecustomers=explore(customers)                      
explorecoupon=explore(coupon)
exploreservice=explore(service)
explorespend=explore(spend)
exploredemo_real=explore(demo_real)

explore=pd.concat([exploredemo_real,explorecoupon,exploreservice,explorespend,explorecustomers],axis=0)
