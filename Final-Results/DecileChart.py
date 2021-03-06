# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:51:23 2018

@author: mm
"""

## Decile chart

probability_df=pd.concat([y_test,probability],axis=1,join='inner')    

## key drivers performance (probability)
for cols in model_table_8.drop(['gold'],axis=1).columns:
    X_test2=pd.DataFrame(X_test[cols])
    probability_df[cols]=X_test2 # to use in decile table as key driver performance

# sort the probability of target for decile table  
probability_df.sort_values(['prob'], ascending=False, inplace=True)
probability_df['prob_cut_10']=pd.qcut(probability_df['prob'],10)
#cuts=probability_df['prob_cut_10'].unique().categories.tolist()
    
decile_table=pd.DataFrame(probability_df.groupby(['prob_cut_10'])['gold'].sum()) 
decile_table.rename(columns={'gold':'target_num'},inplace=True)
decile_table.sort_values(['target_num'],ascending=False,inplace=True)
decile_table['N']=probability_df.groupby(['prob_cut_10'])['gold'].count()                 
decile_table['target_rate'] = decile_table['target_num']/decile_table['N']
decile_table['target_cum']=np.cumsum(decile_table['target_num'])                            
decile_table['target_cum_rate']=np.cumsum(decile_table['target_num'])/np.cumsum(decile_table['N'])                     
decile_table['lift'] = decile_table['target_num']/np.mean(decile_table['target_num'])                     
decile_table['within_target_rate'] = decile_table['target_num']/sum(decile_table['target_num'])                     
decile_table['within_cum_target_rate'] = decile_table['target_cum']/sum(decile_table['target_num'])                       
decile_table['score']=probability_df.groupby(['prob_cut_10'])['prob'].mean()
# mean of probability for each key driver: 
for cols in model_table_8.drop(['gold'],axis=1).columns:
    decile_table[cols]=probability_df.groupby(['prob_cut_10'])[cols].mean()
    
##................plot decile charts................    
# target num chart    
plt.figure()
x = np.arange(10)
plt.bar(x, decile_table['target_num'])
plt.xlim([-1, 10])
plt.ylim([0 , 3500])
plt.xlabel('Deciles')
plt.ylabel('target_num')
plt.title('Target_Num decile chart')
plt.show()                   

from matplotlib.ticker import FuncFormatter
import matplotlib
def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'
# target_rate chart
plt.figure()
x = np.arange(10)
plt.bar(x, decile_table['target_rate'])
plt.xlim([-1, 10])
plt.ylim([0 , 1])
plt.xlabel('Deciles')
plt.ylabel('target_rate')
plt.title('Target_Rate decile chart')
formatter = FuncFormatter(to_percent)
# Set the formatter
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()                        

# lift chart
plt.figure()
x = np.arange(10)
plt.bar(x, decile_table['lift'])
plt.xlim([-1, 10])
plt.ylim([0 , 3])
plt.xlabel('Deciles')
plt.ylabel('lift')
plt.title('Lift decile chart')
plt.show() 