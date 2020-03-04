import pandas as pd
import numpy as np
import scipy.stats as stats
import os

PATH = '/Users/Sarah/Documents/GitHub/final_project/data/merged'
os.listdir(PATH)
df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
df.columns 
small_df = df.drop(columns = ['Unnamed: 0','aod47', 'aod55',
                              'station_name','elevation', 'latitude',
                              'longitude', 'mtd_prcp_normal', 'mtd_snow_normal',
                              'ytd_prcp_normal', 'ytd_snow_normal', 'dly_tavg_normal',
                              'dly_dutr_normal', 'dly_tmax_normal', 'dly_tmin_normal'])

#this merges duplicate (where site name and date is duplicated, these shouldn't exist but seem to)
pm25 = small_df.pivot_table(index='date', columns='site_name', 
                            values='daily_mean_pm_2_5_concentration', 
                            aggfunc='mean')

#need to make site name into col name
#and date into row

#correlation table
pm25.corr()
#[30 rows x 30 columns]

#4TH DISTRICT COURT with CAMP LOGAN TRAILER
pm25.corr().iloc[0,1]
#Output:0.8578030881698346



####
#working
####
#cite: https://towardsdatascience.com/four-ways-to-quantify-synchrony-between-time-series-data-b99136c4a9c9
#from the site: replecated!
test = pd.read_csv('/Users/Sarah/Desktop/synchrony_sample.csv')
test.iloc[0,1]
test.corr().iloc[0,1]
overall_pearson_r = test.corr().iloc[0,1]
print(f"Pandas computed Pearson r: {overall_pearson_r}")
# out: Pandas computed Pearson r: 0.2058774513561943

#let's add a col and see what happens:
#list(range(5400))
test['new'] = list(range(5400))
#Pandas computed Pearson r: 0.2058774513561943
#unchanged!
#In [74]: test.corr().iloc[0,2]                                                                                           
#Out[74]: -0.3149954948945115
#In [75]: test.corr().iloc[1,1]                                                                                           
#Out[75]: 1.0
#In [76]: test.corr().iloc[1,2]                                                                                           
#Out[76]: 0.11373199295203283
test.corr().iloc[1,2]



r, p = stats.pearsonr(test.dropna()['S1_Joy'], test.dropna()['S2_Joy'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# out: Scipy computed Pearson r: 0.20587745135619354 and p-value: 3.7902989479463397e-51



# Compute rolling window synchrony
'''
f,ax=plt.subplots(figsize=(7,3))
test.rolling(window=30,center=True).median().plot(ax=ax)
ax.set(xlabel='Time',ylabel='Pearson r')
ax.set(title=f"Overall Pearson r = {np.round(overall_pearson_r,2)}");
'''
