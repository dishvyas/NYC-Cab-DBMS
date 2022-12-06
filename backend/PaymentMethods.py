from SqlConnector import get_connection3

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def fetch_diff_payment_types(params):
    cursor = get_connection3()
    c = cursor.cursor()

    # start_year = 2018
    # end_year = 2022
    start_year = params['start_year']
    end_year = params['end_year']

    query = f"""
    SELECT (TP11.MONTH || '-' || TP11.YEAR) month_year, TP11.Payment_1, TP22.Payment_2
    FROM
        (SELECT MONTH, YEAR, PaymentType, COUNT(PaymentType) AS Payment_1
        FROM
        (SELECT PaymentID, PaymentType
            FROM Payment WHERE PaymentType = 1) P1
        JOIN
            (SELECT PtoT1.PaymentID,T1.TripID,MONTH,YEAR FROM
                (SELECT TripID, MONTH, YEAR
                FROM TRIP
                WHERE YEAR >= {start_year} AND YEAR <= {end_year}
                GROUP BY MONTH, YEAR, TripID
                ORDER BY YEAR ASC, MONTH ASC, TripID) T1
            JOIN 
                (SELECT TripID, PaymentID
                FROM PassengerToTrip) PtoT1
            ON T1.TripID = PtoT1.TripID)TP1
        ON TP1.PaymentID = P1.PaymentID
        GROUP BY Month,Year,PaymentType) TP11
    JOIN 
        (SELECT MONTH, YEAR, PaymentType, COUNT(PaymentType) AS Payment_2
        FROM
        (SELECT PaymentID, PaymentType
            FROM Payment WHERE PaymentType = 2) P2
        JOIN
            (SELECT PtoT2.PaymentID,T2.TripID,MONTH,YEAR FROM
                (SELECT TripID, MONTH, YEAR
                FROM TRIP
                WHERE YEAR >= {start_year} AND YEAR <= {end_year}
                GROUP BY MONTH, YEAR, TripID
                ORDER BY YEAR ASC, MONTH ASC, TripID) T2
            JOIN 
                (SELECT TripID, PaymentID
                FROM PassengerToTrip) PtoT2
            ON T2.TripID = PtoT2.TripID)TP2
        ON TP2.PaymentID = P2.PaymentID
        GROUP BY Month,Year,PaymentType) TP22
    ON TP11.month = TP22.month AND TP11.year = TP22.year
    ORDER BY TP11.YEAR ASC, TP11.MONTH ASC"""

    data = execute_fetch(c, query)
    cursor.close()
    #print(data)
    return data