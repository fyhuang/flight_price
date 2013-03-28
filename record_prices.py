from __future__ import print_function, unicode_literals, division

import sys
import math
import json
import shelve
import os
from subprocess import check_output
from datetime import date, timedelta
from time import sleep
from contextlib import closing

from flightprice import DAYS_OF_WEEK, Trip, next_day
import parse

def get_trips(num_days, config):
    num_weeks = int(math.ceil(num_days / 7))
    weeks = [date.today()]
    for i in range(num_weeks):
        weeks.append(weeks[-1] + timedelta(7))

    trips = []
    for week in weeks:
        for o in config["origins"]:
            for d in config["destinations"]:
                for day_spec in config["days"]:
                    day = day_spec[0]
                    length = day_spec[1]

                    out_dt = next_day(week, day)
                    in_dt = out_dt + timedelta(length)
                    if (in_dt - date.today()).days < num_days:
                        # Some airlines don't have prices past 180 days
                        trips.append(Trip(o, d, out_dt))
                        trips.append(Trip(d, o, in_dt))

    return trips

def get_prices(trips, db_filename, config):
    """
    DB structure:

    {
        /* Date of search */
        "2013-01-01": {
            /* str(Trip) */
            "SFO:BOS:2013-02-01": [
                FlightInfo(...),
                FlightInfo(...),
                /* ... */
            ]
        },

        "2013-01-02": {
            /* ... */
        }
    }
    """

    wait_time = int(config['wait']) if 'wait' in config else 10
    DATE_FMT = "%Y-%m-%d"
    with closing(shelve.open(db_filename)) as db:
        db_flights = {}

        for trip in trips:
            flights = []

            date_str = trip.date.strftime(DATE_FMT)
            sw_json = check_output(['casperjs',
                'casper/southwest_prices.coffee',
                trip.origin, trip.dest, date_str])
            flights += parse.southwest(sw_json.decode())

            hm_json = check_output(['casperjs',
                'casper/hipmunk_prices.coffee',
                trip.origin, trip.dest, date_str])
            flights += parse.hipmunk(hm_json.decode())

            if len(flights) == 0:
                print("WARNING: no flights returned {}!".format(trip))
            else:
                db_flights[str(trip)] = flights

            sleep(wait_time)


        db[date.today().strftime(DATE_FMT)] = db_flights


def main(args=None):
    if args is None:
        args = sys.argv

    config_filename = args[1]
    with open(config_filename, 'r') as f:
        config = json.load(f)

    trips = get_trips(180, config)

    if not os.path.exists('db'):
        os.makedirs('db')

    get_prices(trips, 'db/prices.db', config)

if __name__ == "__main__":
    main()

"""
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
"""
