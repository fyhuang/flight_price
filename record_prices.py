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
from collections import namedtuple

import parse

days_of_week = {
        'Mon': 0,
        'Tue': 1,
        'Wed': 2,
        'Thu': 3,
        'Friday': 4,
        'Fri': 4,
        'Sat': 5,
        'Sun': 6,
        }

_Trip = namedtuple('Trip', ['origin', 'dest', 'date'])
class Trip(_Trip):
    def __repr__(self):
        return '{}:{}:{}'.format(
                self.origin,
                self.dest,
                self.date.strftime('%Y-%m-%d')
                )

    @classmethod
    def from_str(cls, trip_as_string):
        tokens = trip_as_string.split(':')
        dt = datetime.datetime.strptime(tokens[2]).date()
        t = cls(tokens[0], tokens[1], dt)
        return t


def next_day(week, day):
    TD = timedelta(1)
    day_num = days_of_week[day]
    curr = week + TD
    while curr.weekday() != day_num:
        curr += TD
    return curr

def get_trips(num_days, config):
    num_weeks = int(math.ceil(num_days / 7))
    weeks = [date.today()]
    for i in range(num_weeks):
        weeks.append(weeks[-1] + timedelta(7))

    trips = []
    for week in weeks:
        for o in config["origins"]:
            for d in config["destinations"]:
                for day in config["outbound_days"]:
                    dt = next_day(week, day)
                    if (dt - date.today()).days < num_days:
                        # Some airlines don't have prices past 180 days
                        trips.append(Trip(o, d, dt))

                for day in config["inbound_days"]:
                    dt = next_day(week, day)
                    if (dt - date.today()).days < num_days:
                        trips.append(Trip(d, o, dt))

    return trips

def get_prices(trips, db_filename, config):
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
