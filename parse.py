import json
import collections
from datetime import datetime

FlightInfo = collections.namedtuple('FlightInfo', ['carrier', 'depart_time', 'arrive_time', 'price', 'num_stops'])


def southwest(text):
    flights = json.loads(text)
    def tr(f):
        # f = {'depart_time': '6:05 AM', 'stops': 'Nonstop', 'price': '$227', 'name': 'outbound_flightRow_1', 'arrive_time': '9:40 AM'}
        dt = datetime.strptime(f['depart_time'], '%I:%M %p')
        at = datetime.strptime(f['arrive_time'], '%I:%M %p')
        pr = f['price'].strip('$ ')
        if len(pr) == 0:
            return None

        if f['stops'] == 'Nonstop':
            ns = 0
        else:
            ns = int(f['stops'][0])

        return FlightInfo('southwest', dt.time(), at.time(), int(pr), ns)

    def norm(lst):
        out = []
        for f in lst:
            of = tr(f)
            if of is not None:
                out.append(of)
        return out

    return (norm(flights['outbound']), norm(flights['inbound']))
