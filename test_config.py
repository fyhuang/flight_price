from __future__ import print_function, unicode_literals, division

import sys
import json
from datetime import date, timedelta

from flightprice import next_day, run_casper

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

if 'casperjs_cmd' in config:
    # Try running casper cmd
    output = run_casper(config, [])

    if not output.startswith(b'CasperJS'):
        print("WARNING: can't run casperjs_cmd")
