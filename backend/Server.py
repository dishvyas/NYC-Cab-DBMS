from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from TripToEmployment import fetch_trips_to_employment_map, fetch_employment_details
from FetchRelationCount import get_count
from COVIDcases import fetch_COVID_taxi
from PaymentMethods import fetch_diff_payment_types
from holidays import holiday
from Inflation import inflation
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
    parameters = request.get_json()
    return fetch_employment_details(parameters)

@app.route("/fetch_count", methods=['GET'])
def get_row_count():
    return {"count": get_count()}

@app.route("/holidays", methods=['GET'])
def hol():
    hol=holiday()
    # print(hol)
    return render_template("holidays.html")

@app.route("/COVID", methods=['GET'])
def fetch_COVID_taxi_controller():
    trip_data = fetch_COVID_taxi()
    #print(trip_data)
    return render_template("COVID.html",trip_data=trip_data)

@app.route("/INFLATION", methods=['GET'])
def fetch_Inflation_taxi_controller():
    trip_data = inflation()
    print(trip_data)
    return render_template("Inflation.html",trip_data=trip_data)

@app.route("/payment", methods=['GET'])
def fetch_diff_payment_types_controller():
    print("HERE HERE HERE HERE HERE")
    pay_data = fetch_diff_payment_types()
    print('We got the pay data')
    return render_template("payment.html",result=pay_data)

if __name__ == '__main__':
    app.run(debug='true')

