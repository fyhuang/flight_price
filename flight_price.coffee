page = require('webpage').create()
system = require 'system'

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
                page.includeJs('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                    () ->
                        airline = page.evaluate( () ->
                            return $('.GGJC4XKGBC').first()
                                .clone().children().remove().end()
                                .text()
                        )
                        price = page.evaluate(() ->
                            return $('.GGJC4XKCEC').first().text()
                        )
                        console.log(airline)
                        console.log(price)
                        phantom.exit()
                )
                

# GGJC4XKIWB GGJC4XKAXB
