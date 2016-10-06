// The MIT License (MIT)
//
// Copyright (c) 2016 Eleftherios Anagnostopoulos for Ericsson AB (EU FP7 CityPulse Project)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

var amqp = require('amqplib/callback_api');
var amqpEndpoint = 'amqp://localhost:8007/';
var ampqConnection = null;

var queueName = 'dynamic-bus-scheduling';
var exchange = 'annotated_data';
var routingKey = 'Aarhus.Road.Traffic.195070';
var N3 = require('n3');

var debug = true;

function establishConnection() {
    amqp.connect(amqpEndpoint, function(err, conn) {
        if (err) {
            console.error("[AMQP]", err.message);
            return setTimeout(establishConnection, 1000);
        }
        conn.on("error", function(err) {
            if (err.message !== "Connection closing") {
                console.error("[AMQP] conn error", err.message);
            }
        });
        conn.on("close", function() {
            console.error("[AMQP] reconnecting");
            return setTimeout(establishConnection, 1000);
        });
        console.log("[AMQP] connected");
        ampqConnection = conn;
        whenConnected();
    });
}

function consumer() {
    var ok = ampqConnection.createChannel(on_open);

    function on_open(err, ch) {
        if (err != null) {
            console.error(err.message);
        }
        ch.assertQueue(queueName, {"messageTtl": 600000});
        ch.bindQueue(queueName, exchange, routingKey);

        ch.consume(queueName, function(msg) {
            if (msg !== null) {
                var parser = N3.Parser();
                var triples = [];
                var trafficJam = false;
                var rdfMessage = msg.content.toString();

                parser.parse(rdfMessage, function (error, triple, prefixes) {
                    if (triple) {
                        triples.push(triple);

                        if (true || triple.object.toString() == "http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam") {
                            trafficJam = true;
                        }
                    }
                    else {
                        if (trafficJam) {
                            var eventIdSplit = triples[0].subject.split('#');
                            var eventId = eventIdSplit[1];

                            var eventTypeSplit = triples[0].object.split('#');
                            var eventType = eventTypeSplit[1];

                            var eventSeveritySplit = triples[2].object.split('^^');
                            var severityLevel = eventSeveritySplit[0].split('"')[1];

                            var eventLatSplit = triples[4].object.split('^^');
                            var latitude = parseFloat(eventLatSplit[0].split('"')[1]);

                            var eventLongSplit = triples[5].object.split('^^');
                            var longitude = parseFloat(eventLongSplit[0].split('"')[1]);

                            var eventDateSplit = triples[8].object.split('^^');
                            var date = eventDateSplit[0].split('"')[1];

                            if (debug) {
                                console.log(
                                    "eventId:", eventId,
                                    ", eventType:", eventType,
                                    ", severityLevel:", severityLevel,
                                    ", latitude: ", latitude,
                                    "longitude: ", longitude,
                                    "date: ", date);
                            }
                        }
                    }
                });
            }
        });
    }
}

function whenConnected() {
    consumer();
}

establishConnection();
