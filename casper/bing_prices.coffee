#ignore_images = (requestData, request) ->
#    if ( (/http:\/\/.+?\.(css|png|gif|jpg)/gi).test(requestData['url']) )
#        request.abort()
#casper = require('casper').create({
#    onResourceRequested: ignore_images
#})
casper = require('casper').create()
utils = require('utils')
moment = require 'includes/moment.min.js'

#casper.on 'remote.message', (msg) ->
#    console.log(msg)


# Parsing CLI options
casper.cli.drop 'cli'
casper.cli.drop 'casper-path'
if casper.cli.args.length < 3
    casper.echo('Usage: bing_prices.coffee origin dest date')
    casper.exit 1


origin = casper.cli.args[0]
dest = casper.cli.args[1]

in_date_fmt = 'YYYY-MM-DD'
date_fmt = 'MM/DD/YYYY'
trip_date = moment(casper.cli.args[2], in_date_fmt).format(date_fmt)


flights = []


# For some reason Bing's form requires all this nonsense
casper.start 'http://www.bing.com/travel/flights', ->
    @click "#oneWayLabel"
    @click "#orig1Text"
    @sendKeys "#orig1Text", origin
    @click "#dest1Text"
    @sendKeys "#dest1Text", dest
    @click "#orig1Text"
    @click "#leave1"
    @sendKeys "#leave1", trip_date

    #@fill "form#flt_form", {
    #        vo1: origin,
    #        o: origin,
    #        ve1: dest,
    #        e: dest,
    #        dm1: trip_date,
    #        #bookingBuddy: false,
    #    }

    @click "form#flt_form input.sbmtBtn"

casper.then ->
    @click "form#flt_form input.sbmtBtn"

gather_data = () ->
    casper.page.render('results.png')

    get_flights = (query) ->
        tbodies = $(query).has('tr.result')
        res = []

        tbodies.each(() ->
            el = $(this).children('tr').first()
            get = (el, q) -> el.find(q).first()

            res.push({
                airline: get(el, 'td.airline').text(),
                depart_time: get(el, 'td.leave').text(),
                arrive_time: get(el, 'td.arrive').text(),
                stops: get(el, 'td.stops').text(),
                price: $.trim(get(el, 'span.price').text())
            })
        )

        return res


    flights = casper.evaluate(get_flights, 'table.resultsTable > tbody')


casper.then ->
    @waitWhileVisible 'img#searching', gather_data, gather_data


casper.run ->
    utils.dump(flights)

    this.exit()
