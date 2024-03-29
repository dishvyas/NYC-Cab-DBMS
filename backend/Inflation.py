from SqlConnector import get_connection4

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def inflation(filters):
    cursor = get_connection4()
    c = cursor.cursor()

    start_date = filters['start_year']
    end_date = filters['end_year']
    year = ",".join([start_date.split('-')[-1], end_date.split('-')[-1]])
    query = f"""SELECT EXTRACT(year FROM tpedpickupdatetime) AS pickupyear, 
AVG(Total_Amount) * COUNT(TRIPID)* 230/COUNT(CabdriverID) as SalaryPerMonth
FROM (
SELECT Total_Amount, TripID,cabdriver.CabdriverID, trip.tpedpickupdatetime,infl FROM PAYMENT
JOIN TRIP
ON PaymentID = TRIPID
FULL JOIN Cabdriver
ON trip.cabdriverid = cabdriver.cabdriverid
JOIN Inflation
ON inflationyear = EXTRACT(year FROM tpedpickupdatetime))
GROUP BY EXTRACT(YEAR FROM tpedpickupdatetime)
ORDER BY pickupyear ASC
    """
    data = execute_fetch(c, query)
    cursor.close()
    print(data)
    return data

    