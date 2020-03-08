import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import seaborn as sns
import matplotlib.pyplot as plt

PATH = '/Users/Sarah/Documents/GitHub/final_project/data/merged'
out_path = '/Users/Sarah/Documents/GitHub/final_project/analysis/build'

df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
all_df = pd.read_csv(os.path.join(PATH,'merged_all.csv'))
#df2 = pd.read_csv(os.path.join(PATH,'merged_plus_weekday_season.csv'))
#df.columns 
df.sort_values(by=['latitude','longitude'])
small_df = df.drop(columns = ['Unnamed: 0','aod47', 'aod55',
                              'station_name','elevation', 'latitude',
                              'longitude', 'mtd_prcp_normal', 'mtd_snow_normal',
                              'ytd_prcp_normal', 'ytd_snow_normal', 'dly_tavg_normal',
                              'dly_dutr_normal', 'dly_tmax_normal', 'dly_tmin_normal'])


#need to make site name into col name
#and date into row

#this merges duplicate (where site name and date is duplicated, these shouldn't exist but seem to)
def corro_maker(small_df, variable):
    pm25 = small_df.pivot_table(index='date', columns='site_name', 
                            values=variable, 
                            aggfunc='mean')
    corr_tab  = pm25.corr()
    return corr_tab
#cite https://hackernoon.com/reshaping-data-in-python-fa27dda2ff77


#correlation table
#corr_tab  = pm25.corr()
#[30 rows x 30 columns]
#corr_tab.to_csv(os.path.join(PATH, 'pm25_site_correlation.csv'))

#4TH DISTRICT COURT with CAMP LOGAN TRAILER
#pm25.corr().iloc[0,1]
#Output:0.8578030881698346

def corroplot(small_df, state, variable, variable_name):
    '''
    takes a df of pm25 per site per date 
    the string of a state name (just for labeling)
    the colname of variable of interest (what value is correlated between sites)
    and the string of the variabe name (just for labeling)
    '''
    corr_tab = corro_maker(small_df,variable)
    fig, ax = plt.subplots(figsize=(8,6)) 
    ax = sns.heatmap(
        corr_tab, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True)

    #ax.set_xticklabels(
    #    ax.get_xticklabels(),
    #    rotation=45,
    #    horizontalalignment='right',
    #    fontsize=6)  

    #ax.set_yticklabels(
    #    ax.get_xticklabels(),
    #    fontsize=6)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_yticklabels(' ') #no ticklabels, if want them, comment out and uncomment above
    ax.set_xticklabels(' ') #same here
    ax.set_title("Pearson Correlation Between " +variable_name+ " Sites "+ state)
    fig.tight_layout()
    plt.savefig(os.path.join(out_path, variable_name+"_site_corr_"+state))
    #plt.close()
    plt.show()

#check
corroplot(small_df, "Chicago", 'daily_mean_pm_2_5_concentration', 'pm2.5')


#state-by-state
for state in all_df['state'].unique():
    il = all_df[all_df['state'] == state]
    il.sort_values(by=['latitude','longitude'])
    temp_df2 = il.drop(columns = ['state',
       'station_name', 'elevation', 'latitude', 'longitude', 'mtd_prcp_normal',
       'mtd_snow_normal', 'ytd_prcp_normal', 'ytd_snow_normal',
       'dly_tavg_normal', 'dly_dutr_normal', 'dly_tmax_normal',
       'dly_tmin_normal'])
    corroplot(temp_df2, state, 'daily_mean_pm_2_5_concentration', 'pm2.5') 


#get corrolations
for state in all_df['state'].unique():
    il = all_df[all_df['state'] == state]
    il.sort_values(by=['latitude','longitude'])
    small_df = il.drop(columns = ['state',
       'station_name', 'elevation', 'latitude', 'longitude', 'mtd_prcp_normal',
       'mtd_snow_normal', 'ytd_prcp_normal', 'ytd_snow_normal',
       'dly_tavg_normal', 'dly_dutr_normal', 'dly_tmax_normal',
       'dly_tmin_normal'])
    corr_tab = corro_maker(small_df,'daily_mean_pm_2_5_concentration')
    print("min", state, round(corr_tab.values.min(), 3))
    print("mean", state, round(corr_tab.values.mean(), 3)) 
    #print(state, corr_tab.values.max())


#weather variables apply to all pm25 sites?
il = all_df[all_df['state'] == "CA"]
il.sort_values(by=['latitude','longitude'])
temp_df = il.drop(columns = ['state','daily_mean_pm_2_5_concentration',
       'station_name', 'elevation', 'latitude', 'longitude',
       'mtd_snow_normal', 'ytd_prcp_normal', 'ytd_snow_normal',
       'dly_tavg_normal', 'dly_dutr_normal', 'dly_tmax_normal',
       'mtd_prcp_normal'])
corroplot(temp_df, "CA", 'dly_tmin_normal', "tmin")




#https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec

all_df = df.pivot_table(index='date', columns='site_name', 
                            values=['daily_mean_pm_2_5_concentration','elevation',
       'latitude', 'longitude', 'mtd_prcp_normal', 'mtd_snow_normal',
       'ytd_prcp_normal', 'ytd_snow_normal', 'dly_tavg_normal',
       'dly_dutr_normal', 'dly_tmax_normal', 'dly_tmin_normal'], 
                            aggfunc='mean')

all_corr = all_df.corr()

fig, ax = plt.subplots(figsize=(10,8)) 
ax = sns.heatmap(
    all_corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True)

ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right',
    fontsize=6)  

ax.set_yticklabels(
    ax.get_xticklabels(),
    fontsize=6)
ax.set_ylabel('')
ax.set_xlabel('')
#ax.set_yticklabels(' ') #no ticklabels, if want them, comment out and uncomment above
#ax.set_xticklabels(' ') #same here
ax.set_title("Correlation Between Variables-Sites")
fig.tight_layout()
plt.savefig(os.path.join(out_path, "all_var_site_corr"))
#plt.close()
plt.show()




#df2.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1', 'date','site_name'], inplace = True)
#nope!
#sns.pairplot(df2, hue = 'daily_mean_pm_2_5_concentration')
fig, ax = plt.subplots()
ax.scatter(x = df['date'], y = df['daily_mean_pm_2_5_concentration'])

plt.scatter(x = df2["season"], y = df2['daily_mean_pm_2_5_concentration'])

plt.scatter(x = df2['mtd_prcp_normal'], y = df2['daily_mean_pm_2_5_concentration'])


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




#not working right
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html 
######
#cross-cor
#####
from scipy import signal
pm25 = small_df.pivot_table(index='date', columns='site_name', 
                            values='daily_mean_pm_2_5_concentration', 
                            aggfunc='mean')
pm25.columns
pm25.shape #(365, 30)
#np.correlate(pm25['VILLAGE HALL'], pm25['WASHINGTON HS'], "same")

sig_1 = pm25['4TH DISTRICT COURT']
sig_2 = pm25['CARY GROVE HS']
corr = signal.correlate(sig_1, sig_2, mode = 'same')/128
corr = signal.correlate(sig_1, sig_2)
#replicate
sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
sig_noise = sig + np.random.randn(len(sig))
corr = signal.correlate(sig_noise, np.ones(128), mode='same') / 128

#clock = np.arange(64, len(sig_1), 128)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
ax_orig.plot(sig_1)
#ax_orig.plot(clock, sig_1[clock], 'ro')
ax_orig.set_title('Original signal')
ax_noise.plot(sig_2)
ax_noise.set_title('Signal with noise')
ax_corr.plot(corr)
#ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(0.5, ls=':')
ax_corr.set_title('Cross-correlated with rectangular pulse')
ax_orig.margins(0, 0.1)
fig.tight_layout()
fig.show()



