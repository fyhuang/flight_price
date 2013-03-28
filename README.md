flight\_prices
=============

Scrape flight prices from online sites and analyse them for patterns. Currently supports getting prices from:

* Bing Travel
* Southwest

Quick Start
===========

Use a JSON configuration file to specify which days-of-week and airports to search. For example, this searches flights from San Francisco area (SFO, SJC, and OAK) to Boston (BOS), leaving on Fridays and returning on Sunday (2 days later) or Monday (3 days later):

~~~
{
    "origins": ["SFO", "SJC", "OAK"],
    "destinations": ["BOS"],

    "days": [
        ["Fri", 2],
        ["Fri", 3]
    ]
}
~~~

This config file is available in the sources as `sample_sfotoboston.json`. Record today's prices using:

~~~
python record_prices.py sample_sftoboston.json
~~~

The prices are saved to a file `db/prices.db`. Run the command in your crontab to check prices every day:

~~~
crontab -e

# In editor
@daily cd /home/$username/flight_prices && python record_prices.py config.json
~~~

Verifying your configuration
============================

Sometimes you may want to make sure that `["Fri", 2]` really does mean returning on Sunday. The included `test_config.py` script prints all the trip combinations that your configuration file specifies:

~~~
python test_config.py sample_sfotoboston.json

# Prints:
#
# Trip: SFO -> BOS (Fri); BOS -> SFO (Sun)
# Trip: SFO -> BOS (Fri); BOS -> SFO (Mon)
# Trip: SJC -> BOS (Fri); BOS -> SJC (Sun)
# Trip: SJC -> BOS (Fri); BOS -> SJC (Mon)
# Trip: OAK -> BOS (Fri); BOS -> OAK (Sun)
# Trip: OAK -> BOS (Fri); BOS -> OAK (Mon)
~~~

Notes for Windows Users
=======================

CasperJS provides some [special instructions](http://casperjs.org/installation.html#windows) for those running on Windows. You may have to set the `casperjs_cmd` configuration option (in your JSON config file) to point to `casperjs.bat`; for example:

~~
{
    /* ... */
    "days": [
        /* ... */
    ],

    "casperjs_cmd": "C:\\casperjs\\batchbin\\casperjs.bat"
}
~~~

Querying Saved Prices
=====================

(This functionality is not yet implemented.)
