ignore_images = (requestData, request) ->
    if ( (/http:\/\/.+?\.(css|png|gif|jpg)/gi).test(requestData['url']) )
        request.abort()
casper = require('casper').create({
    onResourceRequested: ignore_images
})
#casper = require('casper').create()
dump = require('utils').dump
moment = require 'includes/moment.min.js'

# Parsing CLI options
casper.cli.drop 'cli'
casper.cli.drop 'casper-path'
if casper.cli.args.length < 3
    casper.echo('Usage: southwest_prices.coffee origin dest date')
    casper.exit 1


origin = casper.cli.args[0]
dest = casper.cli.args[1]

in_date_fmt = 'YYYY-MM-DD'
date_fmt = 'MM/DD/YYYY'
trip_date = moment(casper.cli.args[2], in_date_fmt).format(date_fmt)


flights = []


casper.start 'http://www.southwest.com', ->
    @click "input#oneWay"
    @fill "form#booking_widget_air_form", {
            originAirport: origin,
            originAirport_displayed: origin,
            destinationAirport: dest,
            destinationAirport_displayed: dest,
            outboundDateString: trip_date,
            #returnDateString: trip_date,

            #returnAirport: 'oneWay',
        }
    
    @click 'input#booking_widget_content_row_btn_search'

#casper.start()

#casper.open('http://www.southwest.com/flight/search-flight.html?int=HOMEQBOMAIR', {
#casper.open('http://www.southwest.com/flight/select-flight.html?displayOnly=&disc=pdc%3A1364080764.282000%3AzUZJT5qASOy1lpypPtcjQQ%40A696CE9A2040AB2FE130F4A50AB2F964938AB4FB&ss=0&int=HOMEQBOMAIR&companyName=&cid=', {
#    method: 'post',
#    data: {
#        'originAirport': origin,
#        'destinationAirport': dest,
#        'outboundDateString': trip_date,
#        'returnAirport': 'oneWay'
#    }
#}).then ->
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

    flights = @evaluate(get_flights, 'table#faresOutbound > tbody > tr')

casper.run ->
    dump(flights)
    this.exit()
