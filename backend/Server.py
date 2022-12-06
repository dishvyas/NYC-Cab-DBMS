from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from TripToEmployment import fetch_trips_to_employment_map, fetch_employment_details
from TripToPollutants import fetch_trip_to_pollutants
from FetchRelationCount import get_count
from COVIDcases import fetch_COVID_count, fetch_COVID_taxi
from PaymentMethods import fetch_payment_count, fetch_diff_payment_types
from holidays import holiday
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/fetch_trips_to_employment_map", methods=['POST'])
def fetch_trips_to_employment_map_controller():
    # print('deepak', request.data)
    parameters = request.get_json()
    print(parameters)
    return fetch_trips_to_employment_map(parameters)

@app.route("/fetch_employment_details", methods=['POST'])
def fetch_employment_details_controller():
    print('hitting server')
    parameters = request.get_json()
    return fetch_employment_details(parameters)

@app.route("/fetch_trip_to_pollutants", methods=['POST'])
def fetch_trip_to_pollutants_controller():
    parameters = request.get_json()
    print(parameters)
    return fetch_trip_to_pollutants(parameters)

@app.route("/fetch_count/<query>", methods=['GET'])
def get_row_count(query):
    if(query == 'query4'):
        tables = ['TRIP', 'EmployementStats']
    if(query == 'query5'):
        tables = ['TRIP', 'CO', 'NO2', 'Ozone']
    
    return {"count": get_count(tables)}

@app.route("/holidays", methods=['GET'])
def hol():
    hol=holiday()
    # print(hol)
    return render_template("holidays.html")

@app.route("/COVID_form", methods=['POST','GET'])
def form_info():
    return render_template("COVID_form.html")

@app.route("/COVID", methods=['POST','GET'])
def fetch_COVID_taxi_controller():
    if request.method == 'POST':
        params = request.form
        trip_data = fetch_COVID_taxi(params)
        trip_count = fetch_COVID_count()
        return render_template("COVID.html",trip_data=trip_data, trip_count=trip_count)

@app.route("/payment_form", methods=['POST','GET'])
def form_info2():
    return render_template("payment_form.html")

@app.route("/payment", methods=['POST','GET'])
def fetch_diff_payment_types_controller():
    if request.method == 'POST':
        params = request.form
        pay_data = fetch_diff_payment_types(params)
        pay_count = fetch_payment_count()
        return render_template("payment.html",pay_data=pay_data, pay_count=pay_count)

if __name__ == '__main__':
    app.run(debug='true')

