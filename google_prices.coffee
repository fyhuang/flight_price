page = require('webpage').create()
system = require 'system'

page.onConsoleMessage = (msg, line, source) ->
    console.log('console> ' + msg)

if system.args.length < 3
    console.log 'Usage: flight_prices.coffee date return-date'
    phantom.exit 1
else
    origin = 'SFO'
    dest = 'DEN'
    there_date = system.args[1]
    return_date = system.args[2]

    page.open encodeURI('https://www.google.com/flights/#search;f=' + origin + ';t=' + dest +
        ';d=' + there_date + ';r=' + return_date + ';s=0'),

        (status) ->
            if status isnt 'success'
                console.log 'ERROR'
            else
                page.includeJs('https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                    () ->
                        airlines = page.evaluate( () ->
                            return $('.GGJC4XKGBC')
                                .clone().children().remove().end()
                                .text()
                        )
                        prices = page.evaluate(() ->
                            result = []
                            $('.GGJC4XKCEC').each(() ->
                                result.push(this)
                                console.log(this)
                            )
                            return result
                        )
                        console.log(airlines)
                        console.log(prices)
                        phantom.exit()
                )
