from SqlConnector import get_connection

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    
    return int(data[0][0])

def get_count(tables):
    cursor = get_connection()

    c = cursor.cursor()

    query = f"""SELECT (a.C1 + b.C2) as count FROM (SELECT COUNT(*) as C1 FROM TRIP) a, (SELECT COUNT(*) as C2 FROM EmployementStats) b"""
    inner_variable = 'A'
    external_variable = 'B'
    inner_query = ""
    out_query = ""
    for index, table in enumerate(tables):

        if index != len(tables)-1:
            out_query += f"{inner_variable}{index}.COUNT + "

            inner_query += f"(SELECT COUNT(*) AS COUNT FROM {table}) {inner_variable}{index},"
        else:
            inner_query += f"(SELECT COUNT(*) AS COUNT FROM {table}) {inner_variable}{index}"
            out_query += f"{inner_variable}{index}.COUNT "

    query = f"SELECT ({out_query}) as COUNT FROM {inner_query}"

    data = execute_fetch(c, query)
    cursor.close()
    return data
    

