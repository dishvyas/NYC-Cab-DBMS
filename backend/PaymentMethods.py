from SqlConnector import get_connection3

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def fetch_diff_payment_types():
    cursor = get_connection3()
    c = cursor.cursor()

    start_year = 2018
    end_year = 2022

    query = f"""
    SELECT (MONTH || '-' || YEAR) month_year, PaymentType, COUNT(PaymentType)
    FROM
        (SELECT PaymentID, PaymentType
        FROM Payment) P
    JOIN
        (SELECT PtoT.PaymentID,T.TripID,MONTH,YEAR FROM
            (SELECT TripID, MONTH, YEAR
            FROM TRIP
            GROUP BY MONTH, YEAR, TripID
            ORDER BY YEAR ASC, MONTH ASC, TripID) T
        JOIN 
            (SELECT TripID, PaymentID
            FROM PassengerToTrip) PtoT
        ON T.TripID = PtoT.TripID)TP
    ON TP.PaymentID = P.PaymentID
    WHERE YEAR >= '{start_year}' AND YEAR <= '{end_year}'
    GROUP BY Month, YEAR, PaymentType
    ORDER BY YEAR ASC, MONTH ASC, PaymentType ASC"""

    data = execute_fetch(c, query)
    cursor.close()
    print(data)
    return data