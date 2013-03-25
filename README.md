flight\_prices
=============

Scrape flight prices from online sites and analyse them for patterns. Currently supports getting prices from:

* Hipmunk
* Southwest

Quick Start
===========

Use a JSON configuration file to specify which days-of-week and airports to search. For example, this searches flights from San Francisco area (SFO, SJC, and OAK) to Boston (BOS), leaving on Fridays and returning on Sunday or Monday:

~~~
{
    "origins": ["SFO", "SJC", "OAK"],
    "destinations": ["BOS"],

    "outbound_days": ["Fri"],
    "inbound_days": ["Sun", "Mon"]
}
~~~

Try not to add too many choices, as the number of searches will increase exponentially. Assume this config file is saved as `sfotoboston.json`. Record today's prices using:

~~~
python record_prices.py sftoboston.json
~~~

The prices are saved to a file `db/prices.db`.

Querying Saved Prices
=====================

(This functionality is not yet implemented.)
