from SqlConnector import get_connection2
from flask import render_template
import os

def execute_fetch(conn, query):
    conn.execute(query)
    data = conn.fetchall()
    columns = [x[0] for x in conn.description]
    data = [dict(zip(columns, x)) for x in data]
    conn.close()
    return data



def holiday():
    ch=christ()
    hw=hallow()
    th=thanks()
    # print(hw)
    # print(type(ch))
    # d.close() 
    return ch,hw,th

def christ():
    db = get_connection2()
    d = db.cursor()
    christmas = f""" 
        select christmas from (
            (select count(tripid) as christmas, 1 as rs from (
                (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
                from trip 
                join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2014' and cast(tpepdropoffdatetime as date) <= '31-DEC-2014')
    union
        (select count(tripid), 2 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2015' and cast(tpepdropoffdatetime as date) <= '31-DEC-2015') 
    union(
        select count(tripid), 3 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2016' and cast(tpepdropoffdatetime as date) <= '31-DEC-2016')
    union
        (select count(tripid), 4 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2017' and cast(tpepdropoffdatetime as date) <= '31-DEC-2017')
        union
        (select count(tripid), 5 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2018' and cast(tpepdropoffdatetime as date) <= '31-DEC-2018')
    union
        (select count(tripid), 6 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2019' and cast(tpepdropoffdatetime as date) <= '31-DEC-2019')
    union
        (select count(tripid), 7 as rs from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '25-DEC-2020' and cast(tpepdropoffdatetime as date) <= '31-DEC-2020')
        order by rs)
    """
    ch = execute_fetch(d, christmas)
    print(ch)
    # d.close()
    print(type(ch))
    return ch
    
def thanks():
    db = get_connection2()
    d = db.cursor()
    thanksgiving = f"""
        select Thanksgiving from (
            (select count(tripid) as Thanksgiving, 1 as tg from (
                (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
                from trip 
                join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2014' and cast(tpepdropoffdatetime as date) <= '28-NOV-2014')
    union
        (select count(tripid), 2 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2015' and cast(tpepdropoffdatetime as date) <= '28-NOV-2015')
    union
        (select count(tripid), 3 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2016' and cast(tpepdropoffdatetime as date) <= '28-NOV-2016')
    union 
        (select count(tripid), 4 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2017' and cast(tpepdropoffdatetime as date) <= '28-NOV-2017')
    union
        (select count(tripid), 5 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2018' and cast(tpepdropoffdatetime as date) <= '28-NOV-2018')
    union
        (select count(tripid), 6 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2019' and cast(tpepdropoffdatetime as date) <= '28-NOV-2019')
    union
        (select count(tripid), 7 as tg from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip 
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto 
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '24-NOV-2020' and cast(tpepdropoffdatetime as date) <= '28-NOV-2020')
        order by tg)
    """
    th = execute_fetch(d,thanksgiving)
    print(th) 
    print(type(th))   
    # d.close()
    return th

def hallow():
    db = get_connection2()
    d = db.cursor()
    halloween = f"""
        select Halloween from (
            (select count(tripid) as Halloween, 1 as hw from (
                (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
                from trip
                join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2014' and cast(tpepdropoffdatetime as date) <= '02-NOV-2014')
    union
        (select count(tripid), 2 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2015' and cast(tpepdropoffdatetime as date) <= '02-NOV-2015')
    union
        (select count(tripid), 3 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2016' and cast(tpepdropoffdatetime as date) <= '02-NOV-2016')
    union
        (select count(tripid), 4 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2017' and cast(tpepdropoffdatetime as date) <= '02-NOV-2017')
    union
        (select count(tripid),5 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2018' and cast(tpepdropoffdatetime as date) <= '02-NOV-2018')
    union
        (select count(tripid), 6 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2019' and cast(tpepdropoffdatetime as date) <= '02-NOV-2019')
    union
        (select count(tripid), 7 as hw from (
            (select trip.tripid, passengertotrip.paymentid, trip.tpedpickupdatetime, trip.tpepdropoffdatetime
            from trip
            join passengertotrip on passengertotrip.tripid = trip.tripid ) pto
            join payment on payment.paymentid = pto.paymentid  )
        where cast(tpedpickupdatetime as date) >= '28-OCT-2020' and cast(tpepdropoffdatetime as date) <= '02-NOV-2020')
        order by hw)
    """
    hw = execute_fetch(d,halloween)
    print(hw)
    # d.close()
    return hw