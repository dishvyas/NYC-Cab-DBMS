from SqlConnector import get_connection3
from flask import render_template
import os

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def fetch_COVID_taxi():
    cursor = get_connection3()
    c = cursor.cursor()

    start_month = '1'
    start_year = '2018'
    end_month = '9'
    end_year = '2022'
    first_bound = start_year + '-' + start_month + '-01'
    
    if end_month == '2':
        second_bound = end_year + '-' + end_month + '-28'
    elif end_month == '4' or end_month == '6' or end_month == '9' or end_month == '11':
        second_bound = end_year + '-' + end_month + '-30'
    else:
        second_bound = end_year + '-' + end_month + '-31'

    query = f"""
    SELECT (CASES.MONTH || '-' || CASES.YEAR) month_year,Total_Cases,Trips FROM
        (SELECT EXTRACT(MONTH FROM DATE_OF_INTEREST) AS MONTH, EXTRACT(YEAR FROM DATE_OF_INTEREST) AS YEAR, SUM(CASE_COUNT) AS Total_Cases
        FROM COVID_CASES
        WHERE DATE_OF_INTEREST BETWEEN TO_CHAR(TO_DATE('{first_bound}','YYYY-MM-DD'),'DD-MON-YYYY') AND TO_CHAR(TO_DATE('{second_bound}','YYYY-MM-DD'),'DD-MON-YYYY')
        GROUP BY EXTRACT(MONTH FROM DATE_OF_INTEREST), EXTRACT(YEAR FROM DATE_OF_INTEREST)
        ORDER BY YEAR ASC, MONTH ASC) CASES
    INNER JOIN
        (SELECT COUNT(*) AS TRIPS, MONTH, YEAR
        FROM TRIP
        GROUP BY MONTH, YEAR
        ORDER BY YEAR ASC, MONTH ASC) TAXIS
    ON TAXIS.MONTH = CASES.MONTH AND TAXIS.YEAR = CASES.YEAR"""

    data = execute_fetch(c, query)
    cursor.close()
   # print(data)
    return data