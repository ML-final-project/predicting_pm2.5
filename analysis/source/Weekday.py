import pandas as pd
import os



PATH = '/Users/Sarah/Documents/GitHub/final_project/data/merged'
df = pd.read_csv(os.path.join(PATH,'merged_noaa_pm25_aod.csv'))
df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
df['weekday'] = 0
df.loc[df['day_of_week'].isin(list(range(0, 5))), 'weekday'] = 1

export_df(df, PATH, 'merged_plus_weekday.csv')

