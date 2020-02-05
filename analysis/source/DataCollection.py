import pandas as pd; import numpy as np
from h5py import File as hfile
import xarray as xr; import os
import matplotlib.pylab as plt
from IPython.display import Image
import folium
from datetime import date, timedelta
import math

import ee;
ee.Initialize()

county  = ['Cook']
state   = ['17']
modvars = ['Optical_Depth_047', 'Optical_Depth_055']

for varname in modvars:
    df = pd.DataFrame({'date':[], 'value_':[], 'county':[]})
    counties = ee.FeatureCollection('TIGER/2018/Counties').filter(ee.Filter.inList('NAME', [county[0]])).filter(ee.Filter.inList('STATEFP', [state[0]]))
    collect = ee.ImageCollection("MODIS/006/MCD19A2_GRANULES").filterDate( ee.Date('2010-12-15'), ee.Date('2010-12-31') ).select(varname)
    nomscale = collect.first().projection().nominalScale()

    def calcMean(img): # gets the mean for the area in each individual img
        mean = img.reduceRegion( ee.Reducer.mean(), counties, nomscale ).get(varname)
        return img.set('date', img.date().format('YYYY-MM-dd')).set('mean', mean)

    # map calcMean() across all images in the collection.
    col = collect.map(calcMean)

    # Reduces the images properties to a list of lists, get info, put in dataframe
    result = col.reduceColumns(ee.Reducer.toList(2), ['date', 'mean']).get('list').getInfo()
    df1 = pd.DataFrame(result)
    df1 = df1.rename(columns={0:'date', 1:'value_'})
    df1['county'] = county[0]
    df = pd.concat((df, df1))
    df.to_csv('data/MODIS_%s_cook_2010_Dec15-31.csv'%(varname), sep=',', index=False)

collect = ee.ImageCollection("MODIS/006/MCD19A2_GRANULES").filterDate( ee.Date('2000-02-20'), ee.Date('2019-12-30') ).select(varname)