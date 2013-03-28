from __future__ import print_function, unicode_literals, division

import datetime
from subprocess import check_output
from collections import namedtuple

DAYS_OF_WEEK = {
        'Mon': 0,
        'Tue': 1,
        'Wed': 2,
        'Thu': 3,
        'Friday': 4,
        'Fri': 4,
        'Sat': 5,
        'Sun': 6,
        }

def next_day(week, day):
    TD = datetime.timedelta(1)
    day_num = DAYS_OF_WEEK[day]
    curr = week + TD
    while curr.weekday() != day_num:
        curr += TD
    return curr



FlightInfo = namedtuple('FlightInfo', ['carrier', 'depart_time', 'arrive_time', 'price', 'num_stops', 'add_days'])

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
        dt = datetime.datetime.strptime(tokens[2], "%Y-%m-%d").date()
        t = cls(tokens[0], tokens[1], dt)
        return t



def run_casper(config, args):
    cmd = 'casperjs'
    if 'casperjs_cmd' in config:
        cmd = config['casperjs_cmd']

    output = check_output([cmd] + args)
    return output

