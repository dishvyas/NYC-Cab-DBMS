from SqlConnector import get_connection

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def fetch_trips_to_employment_map(filters):
    cursor = get_connection()
    c = cursor.cursor()
    k = "AND %s='%s'"%('"MONTH"', 'Dec')
    duration = filters['duration']
    start_date = filters['start_date']
    end_date = filters['end_date']
    year = ",".join([start_date.split('-')[-1], end_date.split('-')[-1]])
    query = f"""SELECT
   T1.*,
   ROUND(T2.EMPLOYMENT_COUNT) as EMPLOYMENT_COUNT 
FROM
   (
      SELECT
         {'month_name, month_number,' if (duration=="month") else ""}
         year_name,
         count(*) as number_of_trips 
      FROM
         (
            SELECT distinct
               TRIPID,
            {"To_char(tpedpickupdatetime, 'Mon')  AS month_name, Extract(month FROM tpedpickupdatetime) AS month_number,"if(duration == "month") else ""}

            Extract(year FROM tpedpickupdatetime) AS year_name            


            FROM
               TRIP 
            WHERE
               CAST(TPEDPICKUPDATETIME as date) >=  '{start_date}' 
               and CAST(TPEDPICKUPDATETIME as date) <= '{end_date}' 
         )
      GROUP BY
        {'month_name,month_number,' if (duration == "month") else ""}
         year_name 
   )
   T1 
   INNER JOIN
      (
         SELECT
            COALESCE( SUM(COUNT), 0 ) AS EMPLOYMENT_COUNT,
            {'"MONTH"  AS "MONTH_NAME",' if(duration == "month") else ""}
            "YEAR" as "YEAR_NAME" 
         FROM
            (
               SELECT
                  * 
               FROM
                  EmployementStats 
               WHERE
                  "YEAR" in  ({year})  {k if (duration == 'year') else ""}
            )
         GROUP BY
            {'"MONTH",' if(duration == 'month') else ""}
            "YEAR" 
      )
      T2 
      ON {'T1.month_name = T2.MONTH_NAME AND' if(duration == 'month') else ""}
       T1.YEAR_NAME = T2.YEAR_NAME  
        
    ORDER BY T1.YEAR_NAME {",T1.month_number" if(duration=='month') else ""}  ASC
    """
    print(query)
    data = execute_fetch(c, query)
    cursor.close()
    return data

    
def fetch_employment_details(parameters):
    cursor = get_connection()
    k = "AND %s='%s'"%('"MONTH"', 'Dec')

    c = cursor.cursor()
    duration = parameters['duration']
    if('month' in parameters):
        month = parameters['month']
    else:
        month = ''
    year = parameters['year']
    query = f""" SELECT
    industry_title,
    {"month," if duration == "month" else ""}
    year,
    round(max(count)) AS employee_count
    FROM
        employementstats
    WHERE
        year = '{year}'
        {f" AND month = '{month}' " if (duration == "month") else k}

         
    GROUP BY
        industry_title,
        {f"month," if (duration == "month") else ""}
        year
        
    ORDER BY
    employee_count DESC""" 
    print(query)
    data = execute_fetch(c, query)
    cursor.close()
    return data
    