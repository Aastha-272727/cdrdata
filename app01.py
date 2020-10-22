# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 07:21:00 2020

@author: admin
"""
#All imports for project

import pandas as pd
import numpy as np
import datetime
import re

#All Function would be defined here


# to separate date and time
def date_modifier(data):
  for index in range(len(data)): 
    if re.match("^\d", str(data[index])):
        year = str(data[index][:4])
        month = str(data[index][4:6])
        day = str(data[index][6:])
        data[index] = "-".join([year,month,day])
    else:
        data[index] = np.nan
  return data    

data = ['20190620']



# to convert date in desired format
def datetime_divider(data):
    for index in range(len(data)):
        if (re.match("^\d",str(data[index]))):
            regex = re.compile("\d{1,8}")
            a = regex.findall(str(data[index])) 
            data[index] = [a[0], a[1]]
        else:
            data[index] = [np.nan, np.nan]
            
    return data     

# to convert time in desired format
def time_modifier(data):
    for index in range(len(data)):
        data[index] = str(data[index])
        
        if re.match("^\d", data[index]):
            hours = int(data[index][:2])
            minutes = data[index][2:4]
            sec = data[index][4:]
            
            if hours>=12:
                if hours == 12:
                    hr = str(hours)
            
                else:
                    hr = str(hours-12)
                meridiem = "PM"    
            else:
               if hours == 0:
                hr = str(12)
               else:
                hr = data[index][:2]
               meridiem = "AM"
            data[index] = ":".join([hr,minutes,sec])+ " "+ meridiem
        else:
            data[index] = np.nan
    return data   

def replace_simple_with_Standard_terminology(dataset):
    dataset[5] = dataset[5].replace("Originating", "Outgoing")
    dataset[5] = dataset[5].replace("Terminating","Incoming")
    dataset[267] = dataset[267].replace("Success", "Voice Portal")
    dataset[312] = dataset[312].replace("Shared Call Appearance", "Secondary Device")
    
    return dataset

def remove_Unwanted_data(dataframe):
    for index in range(len(dataframe)):
        if dataframe[index] == "Secondary Device" or dataframe[index] == "Primary Device":
            continue
        else:
            dataframe[index] = np.nan
    return dataframe  

def combine_All_Services(data1, data2, data3):
    for index in range(len(data1)):
        if data1[index] is np.nan:
            if data2[index] is not np.nan and data3[index] is not np.nan:
                data1[index] = str(data2[index])+ "," + str(data3[index])
            elif data2[index] is not np.nan:
                data1[index] = data2[index]
            else:
                data1[index] = data3[index]
        else:
             continue
    return data1 

data1 = ['Primary Device', 'Simultaneous Ring Personal', 'Secondary Device', 'Remote Office', 'Simultaneous Ring Personal']
data2 = ['Primary Device', 'Secondary Device', 'Primary Device', 'Secondary Device', 'Primary Device']
data3 = ['Voice Portal']
result = combine_All_Services(data1, data2, data3)    
print(result)

def call_time_fetcher(data):
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            year = data[index][:4]
            month = data[index][4:6]
            day = data[index][6:8]
            hours = data[index][8:10]
            minutes = data[index][10:12]
            seconds = str(round(float(data[index][12:])))
            if int(seconds) >= 60:
                seconds = int(seconds)-60
                minutes = int(minutes)+1
            if int(minutes) >=60:
                hours = int(hours)+1
                minutes = int(minutes) - 60
            data[index] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"
        else:
            data[index] = np.nan
    return data

def hourly_range(data):
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!= "nan":
            if re.search("PM", data[index]):
                time_data = re.findall("\d+", data[index])
                if time_data[0] != "12":
                    time_data = int(time_data[0]) + 12
                else:
                    time_data = time_data[0]
            else:
                time_data = re.findall("\d+", data[index])
                if int(time_data[0]) == 12:
                    time_data = f"0{int(time_data[0]) - 12}"
                else:
                    time_data = time_data[0]
            data[index] = f"{time_data}:00 - {time_data}:59"
        else:
            data[index] = np.nan
    return data      

def weekly_range(data):
  for index in range(len(data)):
       data[index] = str(data[index])
       if data[index]!= "nan":
           year, month, day = [int(x) for x in data[index].split("-")]
           result = datetime.date(year, month, day)
           data[index] = result.strftime("%A")
       else:
           data[index] = np.nan
  return data

# Main code of your project

dataset_name = 'raw_cdr_data.csv'
raw_cdr_data = pd.read_csv(dataset_name, header = None, low_memory = False)      


#Main code of your project


dataset_name = 'raw_cdr_data.csv'
raw_cdr_data = pd.read_csv(dataset_name, header = None, low_memory = False) 

raw_cdr_data['date'], raw_cdr_data['time'] = \
    zip(*datetime_divider(raw_cdr_data[9].tolist()))
    
print(raw_cdr_data['date'].tolist())
print(raw_cdr_data['time'].tolist())
    



raw_cdr_data['date'] = date_modifier(raw_cdr_data['date'].tolist())
raw_cdr_data['time'] = time_modifier(raw_cdr_data['time'].tolist())

print(raw_cdr_data['date'].tolist())
print(raw_cdr_data['time'].tolist())



raw_cdr_data[5].unique()
raw_cdr_data[267].unique()
raw_cdr_data[312].unique()


raw_cdr_data = replace_simple_with_Standard_terminology(raw_cdr_data)

print(raw_cdr_data[5].unique())
print(raw_cdr_data[267].unique())
print(raw_cdr_data[312].unique())

raw_cdr_data[312].unique()
raw_cdr_data[312] = remove_Unwanted_data(raw_cdr_data[312].tolist())
print(raw_cdr_data[312].unique)

print(raw_cdr_data[147])
raw_cdr_data[147] = combine_All_Services(raw_cdr_data[147].tolist(),
                                         raw_cdr_data[312].tolist(),
                                         raw_cdr_data[267].tolist())

# to find duration

raw_cdr_data["starttime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[9].tolist()))
print(raw_cdr_data["starttime"])
# 2019-06-25 19:24:54

print(raw_cdr_data[13])
raw_cdr_data["endtime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[13].tolist()))
print(raw_cdr_data["endtime"])

# 2019:06:25 19:24:54

raw_cdr_data["duration"] = (raw_cdr_data["endtime"] - raw_cdr_data["starttime"])\
    .astype("timedelta64[m]")
    
print(raw_cdr_data["duration"])

#creates 1 hour range for 24 hours

raw_cdr_data["hourly_range"] = hourly_range(raw_cdr_data["time"].tolist())
print(raw_cdr_data["hourly_range"])
#19:00 - 19:59

#mon to sun
raw_cdr_data["weekly_range"] = weekly_range(raw_cdr_data["date"].tolist())
print(raw_cdr_data["weekly_range"])

#remove columns not required
raw_cdr_data = raw_cdr_data.drop("time", axis = 1)

#save transformed data in CSV format for further use
raw_cdr_data.to_csv("cdr_data.csv", index = None)
    

 

 



     
                  
#










