import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as calander
import glob
import matplotlib.pyplot as plt
import os

def generate_ids(data):
    n = len(data)
    data['tripID'] = np.arange(1, n+1)
    data['cabDriverID'] = np.random.random_integers(size=(n), low=1, high=100000)
    data['passengerID'] = np.random.random_integers(size=(n), low=1, high=230000)
    data['paymentID'] = np.arange(1, n+1)

def divide_schemas(data, save_dir='./preprocessed_data'):
    os.makedirs(save_dir, exist_ok=True)
    passengerToTrip = data[['tripID', 'cabDriverID', 'paymentID']].drop_duplicates()
    passengerToTrip.to_csv(os.path.join(save_dir, 'passenger_to_trip.csv'), index=False)
    passenger = data[['passengerID']].drop_duplicates()
    passenger.to_csv(os.path.join(save_dir, 'passenger.csv'), index=False)
    cabDriver = data[['cabDriverID', 'VendorID']]
    
    cabDriver = cabDriver.drop_duplicates()
    cabDriver.to_csv(os.path.join(save_dir, 'cabdriver.csv'), index=False)
    payment = data[['paymentID', 'payment_type', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'mta_tax', 'extra']]
    payment = payment.drop_duplicates()
    payment.to_csv(os.path.join(save_dir, 'payment.csv'), index=False)
    passengerToTrip = data[['passengerID', 'tripID', 'paymentID']]
    passengerToTrip = passengerToTrip.drop_duplicates()
    passengerToTrip.to_csv(os.path.join(save_dir, 'passenger_to_trip.csv'), index=False)
    trip = data[['tripID', 'doLocationID', 'passengerCount', 'puLocationID', 'month', 'year', 'RatecodeID', 'storeAndFwdFlag', 'tpedPickupDateTime', 'tpepDropoffDateTime', 'cabDriverID']]
    trip.rename({"month": "puMonth", "year": "puYear"})
    trip.to_csv(os.path.join(save_dir, 'trip.csv'), index=False)
    
    
def read_data():
    files = glob.glob('./raw-data/*')
    max_rows = int(2000000/len(files))
    final_data = pd.DataFrame()
    for file in files:
        final_data = pd.concat([pd.read_parquet(file).sample(n=max_rows), final_data])
    return final_data

data = read_data()
data.reset_index(drop=True, inplace=True)
data = data.rename(columns= {"VendorId": "vendorID", "DOLocationID": "doLocationID", "passenger_count": "passengerCount", "PULocationID": "puLocationID", "DOLocationID": "doLocationID", "month": "puMonth", "year": "puYear", "RateCodeID": "rateCodeID", "store_and_fwd_flag": "storeAndFwdFlag","tpep_dropoff_datetime": "tpepDropoffDateTime", "tpep_pickup_datetime": "tpedPickupDateTime" })


tpde = pd.to_datetime(data['tpedPickupDateTime'])
dpde = pd.to_datetime(data['tpepDropoffDateTime'])

data['date'] = tpde.dt.normalize()
data['time'] = tpde.dt.hour
data['weekday'] = data['date'].dt.day_name()
data['duration'] = dpde - tpde
data['duration'] = data['duration'] / np.timedelta64(1, 'm')

cal = calander()
holidays = cal.holidays(start='2018-01-01', end='2018-12-31')
data['holiday'] = data['date'].isin(holidays)
data['week'] = data['date'].dt.dayofweek
data.loc[data['week'] >= 5, 'day_type'] = "weekend"
data.loc[data['week'] < 5, 'day_type'] = "workday"
data.loc[data['holiday'] == True, 'day_type'] = "holiday"
data = data.drop(['holiday', 'week'], axis=1)

def time_slots(x):
    if x in range(6,12):
        return 'Morning'
    elif x in range(12,17):
        return 'Afternoon'
    elif x in range(17,22):
        return 'Evening'
    else:
        return 'Late Night'

data['time_desc'] = data['time'].apply(time_slots)
data = data[(data['passengerCount'] > 0) & (data['passengerCount'] < 7)]

data = data[(data['trip_distance'] > 0) & (data['trip_distance'] <= 100)]

data = data[(data['duration'] > 0) & (data['duration'] <= 180)]

data = data[(data['payment_type'] != 3) & (data['payment_type'] != 4) & (data['payment_type'] != 5) & (data['payment_type'] != 6)]

data = data[(data['fare_amount'] >= 2.5) & (data['fare_amount'] <= 250)]

data = data[(data['puLocationID'] >= 1) & (data['puLocationID'] <= 263) & (data['doLocationID'] >= 1) & (data['doLocationID'] <= 263)]

data['month'] = pd.DatetimeIndex(data['date']).year
data['year'] = pd.DatetimeIndex(data['date']).month

generate_ids(data)
divide_schemas(data)
