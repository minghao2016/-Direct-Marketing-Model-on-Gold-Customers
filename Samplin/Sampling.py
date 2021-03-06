# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:54:18 2018

@author: mm
"""

import pandas as pd
import random
import os

coupon=pd.read_sas('coupon.sas7bdat')
customers=pd.read_sas('customers.sas7bdat')
demo_real=pd.read_sas('demo_real.sas7bdat')
service=pd.read_sas('service.sas7bdat')
spend=pd.read_sas('spend.sas7bdat')
target=pd.read_sas('target.sas7bdat')

# Sampling
#check target frequency
target.gold.value_counts()/len(target) # we use random sampling because target is not parse

import matplotlib.pyplot as plt
plt.figure()
target['gold'].plot(kind="bar", legend=False)
plt.show()

## sample function get the dataframe and sample rate and return the sample data frame                        
def sample(df,samplerate):
    #df: dataframe for sampling
    #samplerate: sample rate 
    #sampledf: final dataframe after random sampling
    rowsnum=df.shape[0]#rows number 
    samplesize=int(rowsnum*samplerate)
    samplenums=random.sample(range(rowsnum), samplesize)
    samplenums.sort()
    sampledf=df.iloc[samplenums]
    return sampledf

# sampling
# sample 30 percent of target data
target=target.dropna(subset=['id'])
targetsample=sample(target,0.3)

# sampling other tables with id indicator achieved by applying sampling on target variable
customerssample=customers.loc[customers['id'] .isin(targetsample.id.tolist())]
couponsample=coupon.loc[coupon['id'] .isin(targetsample.id.tolist())]
servicesample=service.loc[service['id'] .isin(targetsample.id.tolist())]
spendsample=spend.loc[spend['id'] .isin(targetsample.id.tolist())]
# do sampling on deal_real based on postal code
demo_realsample=demo_real.loc[demo_real['POSTCODE'] .isin(customerssample.postcode.tolist())]

# save sampled data
customerssample.to_csv('customerssample.csv')
couponsample.to_csv('couponsample.csv')
servicesample.to_csv('servicesample.csv')
targetsample.to_csv('targetsample.csv')
spendsample.to_csv('spendsample.csv')
demo_realsample.to_csv('demo_realsample.csv')