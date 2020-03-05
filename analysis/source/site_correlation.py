import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import seaborn as sns
import matplotlib.pyplot as plt

PATH = '/Users/Sarah/Documents/GitHub/final_project/data/merged'
out_path = '/Users/Sarah/Documents/GitHub/final_project/analysis/build'
os.listdir(PATH)
df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
df.columns 
small_df = df.drop(columns = ['Unnamed: 0','aod47', 'aod55',
                              'station_name','elevation', 'latitude',
                              'longitude', 'mtd_prcp_normal', 'mtd_snow_normal',
                              'ytd_prcp_normal', 'ytd_snow_normal', 'dly_tavg_normal',
                              'dly_dutr_normal', 'dly_tmax_normal', 'dly_tmin_normal'])

#need to make site name into col name
#and date into row

#this merges duplicate (where site name and date is duplicated, these shouldn't exist but seem to)
pm25 = small_df.pivot_table(index='date', columns='site_name', 
                            values='daily_mean_pm_2_5_concentration', 
                            aggfunc='mean')
#cite https://hackernoon.com/reshaping-data-in-python-fa27dda2ff77


#correlation table
corr_tab  = pm25.corr()
#[30 rows x 30 columns]
corr_tab.to_csv(os.path.join(PATH, 'pm25_site_correlation.csv'))

#4TH DISTRICT COURT with CAMP LOGAN TRAILER
pm25.corr().iloc[0,1]
#Output:0.8578030881698346

fig, ax = plt.subplots(figsize=(10,8)) 
ax = sns.heatmap(
    corr_tab, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right',
    fontsize=6   
)
ax.set_yticklabels(
    ax.get_xticklabels(),
    fontsize=6
)
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_title("Pearson Correlation Between pm25 Sites")
fig.tight_layout()
plt.savefig(os.path.join(out_path, "pm25_site_corr"))
plt.close()



plt.xlabel('xlabel', fontsize=1)
ax.labels('xtick', labelsize=8)    # fontsize of the tick labels
ax.labels('ytick', labelsize=8)

#https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec






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
###
#failed to replicate, not working?

# Set window size to compute moving window synchrony.
r_window_size = 120
# Interpolate missing data.
df_interpolated = test.interpolate()
# Compute rolling window synchrony
rolling_r = df_interpolated['S1_Joy'].rolling(window=r_window_size, center=True).corr(df_interpolated['S2_Joy'])

'''
f,ax=plt.subplots(2,1,figsize=(14,6),sharex=True)
df.rolling(window=30,center=True).median().plot(ax=ax[0])
ax[0].set(xlabel='Frame',ylabel='Smiling Evidence')
rolling_r.plot(ax=ax[1])
ax[1].set(xlabel='Frame',ylabel='Pearson r')
plt.suptitle("Smiling data and rolling window correlation")
'''
