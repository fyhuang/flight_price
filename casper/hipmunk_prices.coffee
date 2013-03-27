ignore_images = (requestData, request) ->
    if ( (/http:\/\/.+?\.(css|png|gif|jpg)/gi).test(requestData['url']) )
        request.abort()
casper = require('casper').create({
    onResourceRequested: ignore_images
})
#casper = require('casper').create()
utils = require('utils')
moment = require 'includes/moment.min.js'

# Parsing CLI options
casper.cli.drop 'cli'
casper.cli.drop 'casper-path'
if casper.cli.args.length < 3
    casper.echo('Usage: hipmunk_prices.coffee origin dest date')
    casper.exit 1


origin = casper.cli.args[0]
dest = casper.cli.args[1]

in_date_fmt = 'YYYY-MM-DD'
date_fmt = 'MMMDD'
trip_date = moment(casper.cli.args[2], in_date_fmt).format(date_fmt)


flights = []

url = utils.format("https://www.hipmunk.com/flights/%s-to-%s#!dates=%s&pax=1",
    origin, dest, trip_date
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


casper.start url, ->
    flights = gather_data()

casper.run ->
    utils.dump(flights)
    this.exit()
