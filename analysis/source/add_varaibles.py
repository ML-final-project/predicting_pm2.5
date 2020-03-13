import pandas as pd
import os
import datetime 
import statsmodels.api as sm


PATH = '/Users/Sarah/Documents/GitHub/final_project/data'
#df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
all_df = pd.read_csv(os.path.join(PATH,'merged/merged_all.csv'))

aod_name = ['Anchorage_047file.csv', 'Anchorage_055file.csv',
            'Arapahoe_047file.csv', 'Arapahoe_055file.csv',
            'Cook_047file.csv', 'Cook_055file.csv', 
            'Hillsborough_047file.csv', 'Hillsborough_055file.csv',
            'Orange_047file.csv', 'Orange_055file.csv']

file_47 = '{}_047file.csv'
file_55 = '{}_055file.csv'
city = ['Anchorage', 'Arapahoe', 'Cook', 'Hillsborough', 'Orange']

def build_fname(base, file):
    return base.format(file)

aod_name_47 = []
for city_name in city:
    aod_name_47.append(build_fname(file_47, city_name))
aod_name_55 = []
for city_name in city:
    aod_name_55.append(build_fname(file_55, city_name))

def add_aod(aod_name, nm):
    aods = []
    for filename in aod_name:
        df = pd.read_csv(os.path.join(PATH, 'AOD/'+filename))
        aods.append(df)

    for i in list(range(len(aods))):
        aods[i].drop(columns = 'aod_type', inplace = True )
        aods[i].rename(columns = {'aod_value': 'aod_value'+nm}, inplace=True)

    concated = aods[0].append(aods[1]).append(aods[2]).append(aods[3]).append(aods[4])
    return concated

'''
for i in [0,2,4,6,8]:
    aods[i].rename(columns = {'aod_value': 'aod_value47'}, inplace=True)

for i in [1,3,5,7,9]:
    aods[i].rename(columns = {'aod_value': 'aod_value55'}, inplace=True)

    temp = aods[0].append(aods[2]).append(aods[4]).append(aods[6]).append(aods[8])
    temp2 = aods[1].append(aods[3]).append(aods[5]).append(aods[7]).append(aods[9])
 '''   


def merge (df1, df2):
    df = df1.merge(df2, on = ["date", "state"], how = 'left')
    return df


merged = merge(all_df, add_aod(aod_name_47, "47"))
df = merge(merged, add_aod(aod_name_55, "55"))


###
#lag
###
df['mtd_prcp_normal_lag'] = df['mtd_prcp_normal'].shift(1)
df['mtd_snow_normal_lag'] = df['mtd_snow_normal'].shift(1)
df['mtd_prcp_normal_lag2'] = df['mtd_prcp_normal'].shift(2)
df['mtd_snow_normal_lag2'] = df['mtd_snow_normal'].shift(2)

###
#add weekday and season
###

df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['weekday'] = 0
df.loc[df['day_of_week'].isin(list(range(0, 5))), 'weekday'] = 1

#season
# date in yyyy/mm/dd format
#Winter (1) begins
#Tuesday, December 21
winter = datetime.datetime(2010, 12, 21) 
#Spring (2) begins
#Saturday, March 20 2010
spring = datetime.datetime(2010, 3, 20) 
#Summer (3) begins
#Monday, June 21
summer = datetime.datetime(2010, 6, 21) 
#Fall (4) begins
#Wednesday, September 22
fall = datetime.datetime(2010, 9, 22) 
#cite https://www.geeksforgeeks.org/comparing-dates-python/ 

df['season'] = 0 
df['date'] = pd.to_datetime(df['date'])



for i in range(len(df['date'])):
    if df['date'][i] >= spring and df['date'][i] < summer:
        df['season'][i] = 2 #spring
    elif df['date'][i] >= summer and df['date'][i] < fall:
        df['season'][i] = 3 #summer
    elif df['date'][i] >= fall and df['date'][i] < winter:
        df['season'][i] = 4 #fall
    else:
        df['season'][i] = 1 #winter


df.to_csv(os.path.join(PATH, 'merged/all_w_aod.csv'))

