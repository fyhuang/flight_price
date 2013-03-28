import sys
import json
from datetime import date, timedelta

from flightprice import next_day

with open(sys.argv[1], "r") as f:
    config = json.load(f)

for o in config["origins"]:
    for d in config["destinations"]:
        for day_spec in config["days"]:
            day = day_spec[0]
            length = day_spec[1]

            out_dt = next_day(date.today(), day)
            in_dt = out_dt + timedelta(length)
            print("Trip: {} -> {} ({}); {} -> {} ({})".format(
                o, d, out_dt.strftime('%a'),
                d, o, in_dt.strftime('%a')
                ))
