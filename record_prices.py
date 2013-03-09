import shelve
from subprocess import check_output
from datetime import date, timedelta
from time import sleep
from contextlib import closing

import parse

FRIDAY = 4

def first_friday():
    TD = timedelta(1)

    dt = date.today()
    dt += TD

    while dt.weekday() != FRIDAY:
        dt += TD
    return dt

fridays = [first_friday()]
for i in range(26): # 6 months
    next_fri = fridays[-1] + timedelta(7)
    # Some airlines don't have prices past 180 days
    if (next_fri - date.today() + timedelta(2)).days < 180:
        fridays.append(next_fri)
    if next_fri.weekday() != FRIDAY:
        print("WARNING: fridays code broken")
sundays = [fri + timedelta(2) for fri in fridays]


with closing(shelve.open('db/prices.db')) as db:
    DATE_FMT = "%Y-%m-%d"
    departures = {}

    for i in range(len(fridays)):
        fstr = fridays[i].strftime(DATE_FMT)
        sstr = sundays[i].strftime(DATE_FMT)

        ob_flights = []
        ib_flights = []

        # Southwest
        sw_json = check_output(['casperjs', 'casper/southwest_prices.coffee', fstr, sstr]).decode()
        sw_flights = parse.southwest(sw_json)

        ob_flights += sw_flights[0]
        ib_flights += sw_flights[1]

        # TODO: other carriers


        if len(ob_flights) == 0 or len(ib_flights) == 0:
            print("WARNING: no flights returned {}:{}!".format(fstr, sstr))
        else:
            departures[fstr] = (ob_flights, ib_flights)

        #sleep(5)


    db[date.today().strftime(DATE_FMT)] = departures
