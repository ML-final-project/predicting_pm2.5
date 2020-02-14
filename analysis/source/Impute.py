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


#
# with open('ChicagoOpticalDepth2010_055nm_line.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     day = 0
#     numDataPtsPerDay = 1
#     for row in csv_reader:
#         if line_count > 0:
#             currentDate = datetime.strptime(row[0], '%Y-%m-%d')
#             currentDateAsInt = timeToInt(currentDate.date())
#             print('Loop is starting, Current date = ' + str(currentDateAsInt) + ', and day = '+str(day))
#         # if we're past the header and we're on the first day (Jan 1st)
#         if (line_count > 0) and (day == 0):
#             print('first day, day = ' + str(day))
#             aod[day] = row[1]
#             day += 1
#         # if we're past the header and the current date is different from the last checked date
#         if (line_count > 0) and (prevDate != currentDate) and (day > 0):
#             # complete the average for the previous day
#             print('here')
#             print('Previous day was day no. ' + str(day) + ', with aod = ' + str(aod[day]))
#             print('Number of data pts in prev day = ' + str(numDataPtsPerDay))
#             aod[day] = aod[day]/numDataPtsPerDay
#             print('after average, previous day aod = ' + str(aod[day]))
#             print('Day = ' + str(day))
#             print('Previous date  = ' + str(prevDateAsInt))
#             print('Current date = ' + str(currentDateAsInt))
#             print(prevDate)
#             print(currentDate)
#             delta = currentDate - prevDate
#             # if there is no data for the next day, store a NaN
#             if currentDate != (prevDate + td(days=1)):
#                 numDaysSkipped = delta.total_seconds()/86400
#                 print('delta = ' + str(numDaysSkipped))
#                 aod[day] =
#                 for i in range(0,int(numDaysSkipped)-1):
#                     print('Currently on day = ' + str(day+i))
#                     aod[day+i] = np.nan
#                 day += int(numDaysSkipped)-1
#                 aod[day] = row[1]
#                 print('day after skip is now = ' + str(day))
#             # else add the new day's data point to the array
#             else:
#                 print('day = ' +str(day))
#                 aod[day] = row[1]
#             # increment the day since we're certain we're on a new day
#             #day += 1
#             # reset the number of points for a given day to one
#             numDataPtsPerDay = 1
#         # if we're past the header and the current date is the same as the last date
#         # (ie multiple values for a single day)
#         elif (line_count > 1) and (prevDate == currentDate) and (day>0):
#             print('value to add = ' + str(row[1]))
#             print('current aod value of day ' + str(day) + ' is  = ' + str(aod[day]))
#             aod[day] = (aod[day] + float(row[1]))
#             numDataPtsPerDay += 1
#         line_count += 1
#         prevDate = currentDate
# print(aod)