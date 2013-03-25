casper = require('casper').create()
utils = require('utils')
moment = require 'includes/moment.min.js'

#casper.on 'remote.message', (msg) ->
#    console.log(msg)


# Parsing CLI options
casper.cli.drop 'cli'
casper.cli.drop 'casper-path'
if casper.cli.args.length < 2
    casper.echo('Usage: hipmunk_prices.coffee date return-date')
    casper.exit 1


origin = 'SFO'
dest = 'DEN'

in_date_fmt = 'YYYY-MM-DD'
date_fmt = 'MMMDD'
there_date = moment(casper.cli.args[0], in_date_fmt).format(date_fmt)
return_date = moment(casper.cli.args[1], in_date_fmt).format(date_fmt)


ob_flights = []
ib_flights = []


#casper.start 'http://www.hipmunk.com', ->
#    @page.render('initial.png')
#    @fill "form#flight", {
#            from0: origin,
#            to0: dest,
#            date0: there_date,
#            date1: return_date,
#        }
#
#    @click "form#flight button.submit"

ob_url = utils.format("https://www.hipmunk.com/flights/%s-to-%s#!dates=%s&pax=1",
    origin, dest, there_date
)

ib_url = utils.format("https://www.hipmunk.com/flights/%s-to-%s#!dates=%s&pax=1",
    dest, origin, return_date
)

gather_data = () ->
    get_flights = (query) ->
        jQuery.fn.justtext = ->
            return $(this).clone().children().remove().end().text()

        items = $(query)
        res = []

        items.each(() ->
            el = $(this).children('div.routing-info').first()
            
            price = el.find('.price-column .price').text().replace(/,/g, '')
            airline = el.find('.airline-column .airline-name').text()
            depart_time = el.find('.graph .depart .inner').justtext()
            arrive_time = el.find('.graph .arrive .inner').justtext()
            stops = el.find('.duration-stop-column .stops').text()

            res.push({
                name: airline,
                depart_time: depart_time,
                arrive_time: arrive_time,
                stops: stops,
                price: price,
            })
        )

        return res


    return casper.evaluate(get_flights, '#sub-graph-1 div.routing')


casper.start ob_url, ->
    @page.render('results.png')
    ob_flights = gather_data()

casper.thenOpen ib_url, ->
    ib_flights = gather_data()


casper.run ->
    utils.dump({
        outbound: ob_flights,
        inbound: ib_flights
    })

    this.exit()
