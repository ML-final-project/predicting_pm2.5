import csv
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from datetime import datetime
from datetime import timedelta as td

aodData = np.zeros(365)
pm25Data = np.zeros(365)
i = 0

with open('047file.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        value = row[1]
        if value == '':
            aodData[i] = np.nan
        else:
            aodData[i] = value
        i += 1
#print(aodData)

i = 0
pm25Data[308] = np.nan
with open('pm25.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if i > 307:
            pm25Data[i+1] = row[4]
        else:
            pm25Data[i] = row[4]
        # print(row[0])
        # print(row[4])
        # print(i)
        # print(pm25Data[i])
        i += 1
#print(pm25Data)

completeData = np.zeros((365,2))
#print(completeData)
for row in range(0,365):
    completeData[row,0] = aodData[row]
    completeData[row,1] = pm25Data[row]

#print(completeData)

imputer = KNNImputer(n_neighbors=4, weights="uniform")
imputedData = imputer.fit_transform(completeData)

#print(imputedData)

currentDate = datetime.strptime('2010-01-01', '%Y-%m-%d')
endDate = datetime.strptime('2011-01-01', '%Y-%m-%d')
f = open('imputed047.csv','w')
nl = '\n'
i = 0

while currentDate < endDate:
    f.write(currentDate.strftime('%Y-%m-%d') + ',' + str(imputedData[i,0]) + nl)
    currentDate = currentDate + td(days=1)
    i += 1
    