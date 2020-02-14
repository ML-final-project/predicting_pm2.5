import csv
import numpy as np
from sklearn import linear_model
from datetime import datetime
from datetime import timedelta as td
import matplotlib.pyplot as plt

def timeToInt(dt_time):
    return 100*dt_time.month + dt_time.day
#datetime.strptime('2012-02-10' , '%Y-%m-%d'

aod = np.zeros(365)

endDate = datetime.strptime('2011-01-01', '%Y-%m-%d')
currentDate = datetime.strptime('2010-01-01', '%Y-%m-%d')
f = open('averaged047.csv','w')
nl = '\n'
# print('here:')
# print(prevDate)
# print(prevDate + td(days = 1))
prevDateAsInt = 101
daysToJump = 1
lastTwoDatesEqual = False

while currentDate < endDate:
    f.write(currentDate.strftime('%Y-%m-%d') + ',' + '' +nl)
    currentDate = currentDate + td(days=1)

f.close()
data = open('ChicagoOpticalDepth2010_047nm_line.csv','r')
data_csv = csv.reader(data, delimiter=',')

value = 0
timesSame = 0;
timesrun = 0;
final_output = open('047file.csv','w')
with open('averaged047.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print('here')
        for data_row in data_csv:
            if data_row[0] == row[0]:
                print('Data row = ' + str(data_row[0]))
                print('row = ' + str(row[0]))
                timesSame +=1
                value += float(data_row[1])
                print(value)
        if value == 0:
            final_output.write(row[0] + ',' + '' + nl)
        else:
            print(str(timesSame))
            value = value/timesSame
            final_output.write(row[0] + ',' + str(value) + nl)
        data.seek(0)
        timesSame = 0
        # timesrun +=1
        # if timesrun == 13:
        #     break
        value = 0


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