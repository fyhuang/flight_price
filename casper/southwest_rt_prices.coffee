#casper = require('casper').create({
#    clientScripts: ['includes/jquery.min.js']
#})
casper = require('casper').create()
dump = require('utils').dump
moment = require 'includes/moment.min.js'

#casper.on 'remote.message', (msg) ->
#    console.log(msg)


# Parsing CLI options
casper.cli.drop 'cli'
casper.cli.drop 'casper-path'
if casper.cli.args.length < 2
    casper.echo('Usage: southwest_prices.coffee date return-date')
    casper.exit 1


origin = 'SFO'
dest = 'DEN'

in_date_fmt = 'YYYY-MM-DD'
date_fmt = 'MM/DD/YYYY'
there_date = moment(casper.cli.args[0], in_date_fmt).format(date_fmt)
return_date = moment(casper.cli.args[1], in_date_fmt).format(date_fmt)


ob_flights = []
ib_flights = []


casper.start 'http://www.southwest.com', ->
    @fill "form#booking_widget_air_form", {
            originAirport: origin,
            destinationAirport: dest,
            outboundDateString: there_date,
            returnDateString: return_date,

            returnAirport: 'RoundTrip',
        }
    
    @click '#booking_widget_content_row_btn_search'

casper.then ->
    get_flights = (query) ->
        rows = $(query)
        results = []
        rows.each(() ->
            el = $(this)
            get = (q) -> el.find(q).first()
            results.push({
                name: el.attr('id'),
                depart_time: get('td:eq(0) > .bugText').text(),
                arrive_time: get('td:eq(1) > .bugText').text(),
                stops: get('td.routing_column a.bugLinkRouting').text(),
                price: $.trim(get('td.price_column:eq(2) .product_price').text())
            })
        )
        return results


    ob_flights = ob_flights.concat(
        @evaluate(get_flights, 'table#faresOutbound > tbody > tr')
    )

    ib_flights = ib_flights.concat(
        @evaluate(get_flights, 'table#faresReturn > tbody > tr')
    )

casper.run ->
    dump({
        outbound: ob_flights,
        inbound: ib_flights
    })

    this.exit()
