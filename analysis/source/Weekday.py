import pandas as pd
import os
import datetime 
import statsmodels.api as sm


PATH = '/Users/Sarah/Documents/GitHub/final_project/data/merged'
df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
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


df.to_csv(os.path.join(PATH, 'merged_plus_weekday_season.csv'))


