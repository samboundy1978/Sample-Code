'''
I have a FitBit, and have had one for several years.

Initially I want to download all my historical data and do some analysis on it.

Instructions on how to do this are here:
https://help.fitbit.com/articles/en_US/Help_article/1133

In this script I plan on inspecting the data I have downloaded, a visual inspection shows the following format:

username
	|-------challenges
	|-------female-health
	|-------messages
	|	|-------FRIEND Conversations
	|
	|-------products-service
	|-------sleep-score
	|-------user-profile
	|	|-------Media
	|
	|-------user-site-export


The data I want is in user-site-report. This folder is a series of JSON files, either:
a name (with _ as seperators)
a name (with _ as seperators) followed by - then a number
a name (with _ as seperators) followed by - then a date

To start with I want to see just what data files FitBit has
'''

###

#Data downlaaded: 11/1/2019
# user-site-export contains: 1919 files
###

import os
import pandas as pd


#All files in directory are 'json, make a list of all .json files
path = 'C:/Users/Sam/Desktop/Python/My projects/FitBit/SamBoundy/user-site-export/'
data_files = [f for f in os.listdir(path) if f.endswith('.json')]

#File structure is name_name-date or number .json, want to remove all but the name
file_types = [f.split('-')[0] for f in data_files]
file_types = [f.split('.')[0] for f in file_types]
file_types_unique = list(set(file_types))

#print the unique types of data files
print('Names and number of all data file in PATH directory')
print(data_files)
print(len(data_files))
print('unique types of files, and number of them')
print(file_types_unique)
print(len(file_types_unique))

#create a .csv file for each type of data file
for type in file_types_unique:
    counter = 0 #Need to add a header. .json format is dateTime, value
    for file in os.listdir(path):

        if type in file:
            if file.startswith(type): #heart_rate occurs as file type and as a part of some file types so need this to only get heart_rate


                if counter == 0:
                    counter += 1
                    print(file)
                    df = pd.read_json(path+file)
                    df.to_csv('C:/Users/Sam/Desktop/Python/My projects/FitBit/results_' +type +'.csv', mode='a', index=False, header=True) #first file has header
                    #print('0 loop'+str(counter))
                else:
                    print(file)
                    df = pd.read_json(path + file)
                    df.to_csv('C:/Users/Sam/Desktop/Python/My projects/FitBit/results_' +type +'.csv', mode='a', index=False, header=False) #all subsequent files have no header
                    #print('not 0 loop'+str(counter))




