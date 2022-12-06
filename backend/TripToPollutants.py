from SqlConnector import get_connection

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data

def fetch_trip_to_pollutants(filters):
    cursor = get_connection()
    c = cursor.cursor()
    duration = filters['duration']
    start_date = filters['start_date']
    end_date = filters['end_date']
    year = ",".join([start_date.split('-')[-1], end_date.split('-')[-1]])
    query = f"""SELECT TR.*, TL.NO2_Concentration, TL.Ozone_Concentration, TL.CO_Concentration FROM (
        
            SELECT  {'month_name, month_number,' if (duration=="month") else ""}

            
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
    TR

    INNER JOIN

    (SELECT T1.*, T2.NO2_Concentration, T3.Ozone_Concentration
    FROM 
    (SELECT COALESCE( AVG(Concentration), 0 ) AS CO_Concentration,
            {'"MONTH" AS "MONTH_NAME",' if (duration == "month") else ""}

            "YEAR" as "YEAR_NAME" 
            FROM
            (
                SELECT
                    * 
                FROM
                    CO 
                WHERE
                    "YEAR" in  ({year})
            )
            GROUP BY
                {'"MONTH",' if(duration == 'month') else ""}

            "YEAR")  T1,

    (SELECT COALESCE( AVG(Concentration), 0 ) AS NO2_Concentration,
            {'"MONTH" AS "MONTH_NAME",' if (duration == "month") else ""}
            "YEAR" as "YEAR_NAME" 
            FROM
            (
                SELECT
                    * 
                FROM
                    NO2 
                WHERE
                    "YEAR" in   ({year})
            )
            GROUP BY
                {'"MONTH",' if(duration == 'month') else ""}
            "YEAR" ) T2,
    
    (SELECT COALESCE( AVG(Concentration), 0 ) AS Ozone_Concentration,
            {'"MONTH" AS "MONTH_NAME",' if (duration == "month") else ""}
            "YEAR" as "YEAR_NAME" 
            FROM
            (
                SELECT
                    * 
                FROM
                    Ozone 
                WHERE
                    "YEAR" in  ({year})
            )
            GROUP BY
                {'"MONTH",' if(duration == 'month') else ""}
            "YEAR") T3 
            
            
            WHERE (  {'T1.MONTH_NAME = T2.MONTH_NAME AND' if(duration == 'month') else ""} T1.YEAR_NAME = T2.YEAR_NAME
            AND  {'T1.MONTH_NAME = T3.MONTH_NAME AND' if(duration == 'month') else ""}  T1.YEAR_NAME = T3.YEAR_NAME)) TL
            ON {'TL.MONTH_NAME = TR.MONTH_NAME AND' if(duration == 'month') else ""} TL.YEAR_NAME = TR.YEAR_NAME

                ORDER BY TR.YEAR_NAME {",TR.month_number" if(duration=='month') else ""}  ASC

    """
    print(query)
    data = execute_fetch(c, query)
    cursor.close()
    return data