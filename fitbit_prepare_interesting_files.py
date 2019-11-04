'''
fitbit_file_set-up.py turns the .json raw data files into a single .csv for each variable recorded and shared by FitBit.

Some of these files are more useful for practicing data science techniques than others.

1) I want to get the head and dtypes for each .csv file and decide which ones will be useful

2) adjust the column titles and variable types, dateTime column needs to be in datetime format, the 'value' column
would be more useful named for the type of variable

NB were I doing this on a better system this would be run as part of the 'fitbit_file_set-up.py' script, but building
the .csv files is time consuming and it is more efficient to run this as two scripts rather than redo the creation of
the .csv files
'''

import pandas as pd
from datetime import datetime
from datetime import timedelta
import os
import numpy as np


#file paths used
path ='C:/Users/Sam/Desktop/Python/My projects/FitBit/'
path_raw = 'C:/Users/Sam/Desktop/Python/My projects/FitBit/SamBoundy/user-site-export/'

#I don't need the code below now

#need the unique data type identifiers used in naming file
data_files = [f for f in os.listdir(path_raw) if f.endswith('.json')]

#File structure is name_name-date or number .json, want to remove all but the name
file_types = [f.split('-')[0] for f in data_files]
file_types = [f.split('.')[0] for f in file_types]
file_types_unique = list(set(file_types))

#print the unique types of data files
print('unique types of files, and number of them')
print(file_types_unique)
print(len(file_types_unique))

#want to see the .head() and .dtypes for each of the .csv files generated in fitbit_file_set-up.py
# some of these files are 10s or 100s of MB, it would be best to only take the first 5 lines.
for type in file_types_unique:
    df = pd.read_csv(path + 'results_' + type +'.csv', nrows = 5)
    print('###\n\ndata type: ' + type)
    print(df.head())
    print(df.dtypes)

'''
file types:
['sedentary_minutes', 'food_logs', 'trophy', 'heart_rate', 'calories', 'time_in_heart_rate_zones', 'water_logs',
'steps', 'badge', 'moderately_active_minutes', 'demographic_vo2_max', 'sleep', 'lightly_active_minutes', 'altitude',
'exercise', 'resting_heart_rate', 'weight', 'height', 'very_active_minutes', 'distance', 'swim_lengths_data']

file types I'm interested in:
['heart_rate', 'steps', 'distance']

###

data type: heart_rate
              dateTime                         value
0  2017-11-07 02:33:30  {'bpm': 84, 'confidence': 0}
1  2017-11-07 02:33:35  {'bpm': 89, 'confidence': 0}
2  2017-11-07 02:33:40  {'bpm': 82, 'confidence': 1}
3  2017-11-07 02:33:55  {'bpm': 82, 'confidence': 1}
4  2017-11-07 02:34:10  {'bpm': 68, 'confidence': 1}
dateTime    object
value       object
dtype: object
###

data type: steps
              dateTime  value
0  2016-06-30 22:19:00      0
1  2016-06-30 22:20:00      0
2  2016-06-30 22:22:00      0
3  2016-06-30 22:23:00      0
4  2016-06-30 22:24:00      0
dateTime    object
value        int64
dtype: object
###

data type: distance
              dateTime  value
0  2016-06-30 22:19:00      0
1  2016-06-30 22:20:00      0
2  2016-06-30 22:22:00      0
3  2016-06-30 22:23:00      0
4  2016-06-30 22:24:00      0
dateTime    object
value        int64
dtype: object
###

For steps and distance I want to change dateTime column to datetime from object and rename value column as data type

heart_rate needs both of those changes and {'bpm': 84, 'confidence': 0} wants to be cut down to only the bpm value

1) all three files need the value and datetime change so do all as a loop
2) fix the bpm column

'''

interesting_types = ['steps', 'distance', 'heart_rate']
#The following is now done

#build csv files for the data types I want to analyze further
#interesting_types = ['steps', 'distance', 'heart_rate']

for type in interesting_types:
    #open steps file with dateTime column in datetime format
    csv = pd.read_csv(path + 'results_' + type + '.csv', parse_dates=['dateTime'])

    #time is in UTC, want to change it to EST (-5 hrs)
    csv['dateTime'] = csv['dateTime']-timedelta(hours=5)

    #rename value column
    csv.rename(columns = {'value':type}, inplace = True)
    csv.to_csv(path + 'analyzable_' + type + '.csv', mode='w', index=False)


#check how this worked
# some of these files are 10s or 100s of MB, it would be best to only take the first 5 lines.
for type in interesting_types:
    df = pd.read_csv(path + 'analyzable_' + type +'.csv', nrows = 5, parse_dates=['dateTime'])
    print('###\n\ndata type: ' + type)
    print(df.head())
    print(df.dtypes)

###

#WHEN OPENING CSV FILE TO DATAFRAME INCLUDE THE DATETIME FUNCTION

###

#fix the heart_rate value column
'''
file format:
dateTime,heart_rate
2017-11-06 21:33:30,"{'bpm': 84, 'confidence': 0}"

want 84 as integer
.split on ' ' pos[1]
.split on ',' pos[0]
'''
#open heart_rate .csv and extract the heart rate at each time as an integer:
csv_heart_rate = pd.read_csv(path + 'analyzable_heart_rate.csv', parse_dates=['dateTime'])
csv_heart_rate['heart_rate'] = [l.split(' ')[1] for l in csv_heart_rate['heart_rate']] #using line by line function as not enough memory to do it in one go
csv_heart_rate['heart_rate'] = [l.split(',')[0] for l in csv_heart_rate['heart_rate']]
csv_heart_rate['heart_rate'] = csv_heart_rate['heart_rate'].astype(np.int64)

#write over the original analyzed heart rate file
csv_heart_rate.to_csv(path + 'analyzable_heart_rate.csv', mode='w', index=False)

