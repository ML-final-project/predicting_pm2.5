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
        