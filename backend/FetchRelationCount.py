from SqlConnector import get_connection

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    
    return int(data[0][0])

def get_count():
    cursor = get_connection()

    c = cursor.cursor()
    
    query = f""" SELECT COUNT(*) FROM TRIP""" 
    data = execute_fetch(c, query)
    cursor.close()
    print(data)
    return data
    