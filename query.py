import shelve
import collections
from contextlib import closing
from datetime import time, datetime, timedelta

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

print("Loading...")
with closing(shelve.open('db/prices.db', 'r')) as db:
    # Compute # weeks in advance to buy tickets
    advance_prices = collections.defaultdict(lambda: [])

    for record_date, departures in db.items():
        for ddate, v in departures.items():
            ob_flights = v[0]
            ib_flights = v[1]

            obf = pick_ob_flight(ob_flights)
            ibf = pick_ib_flight(ib_flights, obf.carrier)
            total_price = obf.price + ibf.price

            weeks_before = (date_from_str(ddate) - date_from_str(record_date) + timedelta(6)).days // 7
            advance_prices[weeks_before].append(total_price)

    advance_avg_price = [(wb, sum(lst) / len(lst)) for wb,lst in advance_prices.items()]
    best_advance_price = min(advance_avg_price, key=lambda wp: wp[1])

    print("Optimal to buy:")
    print("# weeks before: {} (${})".format(best_advance_price[0], best_advance_price[1]))
