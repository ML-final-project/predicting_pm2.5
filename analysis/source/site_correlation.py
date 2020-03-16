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
def corrolation (all_df, variable):
    for state in all_df['state'].unique():
        il = all_df[all_df['state'] == state]
        il.sort_values(by=['latitude','longitude'])
        small_df = il.drop(il.columns.difference([variable,
                        'date', 'site_name']), 1) 
        corr_tab = corro_maker(small_df, variable)
        #print(variable)
        print("min", state, round(corr_tab.values.min(), 3), "mean", state, round(corr_tab.values.mean(), 3))
        #print("mean", state, round(corr_tab.values.mean(), 3)) 
        #print(state, corr_tab.values.max())

#corrolation(all_df, 'daily_mean_pm_2_5_concentration')
#cite: https://stackoverflow.com/questions/45846189/how-to-delete-all-columns-in-dataframe-except-certain-ones 

cols = ['daily_mean_pm_2_5_concentration', 
        'mtd_prcp_normal',
       'mtd_snow_normal', 'ytd_prcp_normal', 'ytd_snow_normal',
       'dly_tavg_normal', 'dly_dutr_normal', 'dly_tmax_normal',
       'dly_tmin_normal']
for i in cols: 
    print(i)
    corrolation(all_df, i)


#summary statistics table 
for state in all_df['state'].unique():
    ca = all_df[all_df['state'] == state]
    ca_stats = pd.DataFrame({"mean" : round(ca.mean(),3)})      
    ca_stats["min"] = ca.min()
    ca_stats["max"] = ca.max()
    ca_stats.drop(["daily_mean_pm_2_5_concentration",'latitude','longitude'],
                axis = 0, inplace = True)
    ca_stats.to_csv(os.path.join(out_path, state+'_NOAA_stats.csv'))




#cite: https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec

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


#cite: https://towardsdatascience.com/four-ways-to-quantify-synchrony-between-time-series-data-b99136c4a9c9








