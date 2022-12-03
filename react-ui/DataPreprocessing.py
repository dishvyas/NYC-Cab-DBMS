import pandas as pd
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as calander
import glob
import matplotlib.pyplot as plt
def generate_ids(data):
    n = len(data)
    data['tripID'] = np.arange(1, n+1)
    data['cabDriverID'] = np.random.random_integers(size=(n), low=1, high=100000)
    data['passengerID'] = np.random.random_integers(size=(n), low=1, high=230000)
    data['paymentID'] = np.arange(1, n+1)

def divide_schemas(data):
    passengerToTrip = data[['tripID', 'cabDriverID', 'paymentID']].drop_duplicates()
    passenger = data[['passengerID']].drop_duplicates()
    cabDriver = data[['cabDriverID', 'vendorID']]
    cabDriver = cabDriver.drop_duplicates()
    payment = data[['paymentId', 'payment_type', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'mta_tax', 'extra']]
    payment = payment.drop_duplicates()
    passengerToTrip = data[['passengerID', 'tripID', 'paymentID']]
    passengerToTrip = passengerToTrip.drop_duplicates()
    passengerToTrip = passengerToTrip.drop_duplicates()
    trip = data[['tripID', 'doLocationID', 'passengerCount', 'puLocationID', 'month', 'year', 'rateCodeID', 'storeAndFwdFlag', 'tpedPickupDateTime', 'tpepDropoffDateTime', 'cabDriverId']]
    trip.rename({"month": "puMonth", "year": "puYear"})
    
    
def read_data():
    files = list(map(lambda x: './raw-data/'+x, ['yellow_tripdata_2018-01.parquet', 'yellow_tripdata_2018-02.parquet', 'yellow_tripdata_2018-03.parquet', 'yellow_tripdata_2018-04.parquet']))
    final_data = pd.DataFrame()
    for file in files:
        final_data = pd.concat([pd.read_parquet(file), final_data])
    return final_data

data = read_data()
data.rename({"VendorId": "vendorID", "DOLocationID": "doLocationID", "passenger_count": "passengerCount", "PULocationID": "puLocationID", "DOLocationID": "doLocationID", "month": "puMonth", "year": "puYear", "RateCodeID": "rateCodeID", "store_and_fwd_flag": "storeAndFwdFlag","tpep_dropoff_datetime": "tpepDropoffDateTime", "tpep_pickup_datetime": "tpedPickupDateTime" })

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

data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month

divide_schemas(data)


# import cx_Oracle
# cx_Oracle.connect( user="d.rangaraju", password="3cbfrLvxQ7YtmdNjTFYVeoaK", dsn="oracle.cise.ufl.edu/d.rangaraju", port=1521)
# export PATH=/Users/deepakraju/instantclient/instantclient_19_8:$PATH
# export ORACLE_HOME=/Users/deepakraju/instantclient/instantclient_19_8
# export DYLD_LIBRARY_PATH=/Users/deepakraju/instantclient/instantclient_19_8
# export OCI_LIB_DIR=/Users/deepakraju/instantclient/instantclient_19_8
# export OCI_INC_DIR=/Users/deepakraju/instantclient/instantclient_19_8/sdk/include
