import sys
import shelve
import collections
from contextlib import closing
from datetime import time, datetime, timedelta

from flightprice import Trip

def date_from_str(s):
    return datetime.strptime(s, '%Y-%m-%d').date()

def pick_flight_bounds(in_flights, after_time, before_time):
    def price_or_none(f):
        if f is not None:
            return f.price
        return 9999 # placeholder price for None

    flights = sorted(in_flights, key=price_or_none)
    for f in flights:
        if f.depart_time >= after_time and f.depart_time <= before_time:
            return f

    raise RuntimeError('No flights matched')

def pick_ob_flight(in_flights):
    after_time = time(16,0)
    before_time = time(23,0)
    return pick_flight_bounds(in_flights, after_time, before_time)

def pick_ib_flight(in_flights, carrier):
    after_time = time(16,0)
    before_time = time(23,0)
    return pick_flight_bounds(in_flights, after_time, before_time)

origin = sys.argv[1]

print("Loading...")
with closing(shelve.open('db/prices.db', 'r')) as db:
    # Compute # weeks in advance to buy tickets
    advance_prices_ob = collections.defaultdict(lambda: [])
    advance_prices_ib = collections.defaultdict(lambda: [])

    # Pick an outbound flight
    for record_date, trips in db.items():
        for trip_str, flights in trips.items():
            trip = Trip.from_str(trip_str)
            weeks_before = (trip.date - date_from_str(record_date) + timedelta(6)).days // 7

            if trip.origin == origin:
                obf = pick_ob_flight(flights)
                advance_prices_ob[weeks_before].append(obf.price)
            else:
                ibf = pick_ib_flight(flights, None)
                advance_prices_ib[weeks_before].append(ibf.price)


for price_dict in (advance_prices_ob, advance_prices_ib):
    advance_avg_price = [(wb, sum(lst) / len(lst)) for wb,lst in price_dict.items()]
    best_advance_price = min(advance_avg_price, key=lambda wp: wp[1])

    print("Optimal to buy:")
    print("# weeks before: {} (${})".format(best_advance_price[0], best_advance_price[1]))
