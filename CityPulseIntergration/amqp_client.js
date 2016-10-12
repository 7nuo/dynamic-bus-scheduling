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
// var amqpEndpoint = 'amqp://localhost:8007/';
var ampqConnection = null;

var queueName = 'dynamic-bus-scheduling';
// var exchange = 'annotated_data';
var exchange = 'events';
var routingKey = '#';
// var routingKey = 'Aarhus.Road.Traffic.201345';
// var routingKey = 'Aarhus.Road.Traffic.195070';
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

// [ { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//     predicate: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
//     object: 'http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam',
//     graph: '' },
//     { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//         predicate: 'http://purl.oclc.org/NET/UNIS/sao/ec#hasSource',
//         object: '"USER_testuser"',
//         graph: '' },
//     { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//         predicate: 'http://purl.oclc.org/NET/UNIS/sao/sao#hasLevel',
//         object: '"2"^^http://www.w3.org/2001/XMLSchema#long',
//         graph: '' },
//     { subject: '_:b0',
//         predicate: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
//         object: 'http://www.w3.org/2003/01/geo/wgs84_pos#Instant',
//         graph: '' },
//     { subject: '_:b0',
//         predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lat',
//         object: '"56.1155615424"^^http://www.w3.org/2001/XMLSchema#double',
//         graph: '' },
//     { subject: '_:b0',
//         predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lon',
//         object: '"10.1870405674"^^http://www.w3.org/2001/XMLSchema#double',
//         graph: '' },
//     { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//         predicate: 'http://purl.oclc.org/NET/UNIS/sao/sao#hasLocation',
//         object: '_:b0',
//         graph: '' },
//     { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//         predicate: 'http://purl.oclc.org/NET/UNIS/sao/sao#hasType',
//         object: 'http://purl.oclc.org/NET/UNIS/sao/ec#TransportationEvent',
//         graph: '' },
//     { subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd',
//         predicate: 'http://purl.org/NET/c4dm/timeline.owl#time',
//         object: '"2016-10-11T11:13:21.000Z"^^http://www.w3.org/2001/XMLSchema#dateTime',
//         graph: '' } ]

function consumer() {
    var ok = ampqConnection.createChannel(on_open);

    function on_open(err, ch) {
        if (err != null) {
            console.error(err.message);
        }
        ch.assertQueue(queueName, {"messageTtl": 600000, "autoDelete": true, "durable": false});
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

                        if (triple.object.toString() == "http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam") {
                            trafficJam = true;
                        }
                    }
                    else {
                        if (trafficJam) {
                            var eventID, eventType, eventLevel, eventLatitude, eventLongitude, eventDate;
                            console.log(triples);

                            for (var i = 0; i < triples.length; i++) {
                                triple = triples[i];

                                // subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd'
                                // predicate: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
                                // object: 'http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam'
                                if (triple.object.toString() == "http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam") {
                                    var subjectSplit = triple.subject.split('#');
                                    eventID = subjectSplit[1];
                                    eventType = "TrafficJam";
                                }
                                else {
                                    var predicateEnding = triple.predicate.split('#')[1];

                                    // predicate: 'http://purl.oclc.org/NET/UNIS/sao/sao#hasLevel'
                                    // object: '"2"^^http://www.w3.org/2001/XMLSchema#long'
                                    if (predicateEnding == "hasLevel") {
                                        var objectSplit = triple.object.split('^^');
                                        eventLevel = objectSplit[0].split('"')[1];
                                    }
                                    // predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lat'
                                    // object: '"56.1155615424"^^http://www.w3.org/2001/XMLSchema#double'
                                    else if (predicateEnding == "lat") {
                                        var objectSplit = triple.object.split('^^');
                                        eventLatitude = parseFloat(objectSplit[0].split('"')[1]);
                                    }
                                    // predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lon'
                                    // object: '"10.1870405674"^^http://www.w3.org/2001/XMLSchema#double'
                                    else if (predicateEnding == "lon") {
                                        var objectSplit = triple.object.split('^^');
                                        eventLongitude = parseFloat(objectSplit[0].split('"')[1]);
                                    }
                                    // predicate: 'http://purl.org/NET/c4dm/timeline.owl#time'
                                    // object: '"2016-10-11T11:13:21.000Z"^^http://www.w3.org/2001/XMLSchema#dateTime'
                                    else if (predicateEnding == "time") {
                                        var objectSplit = triple.object.split('^^');
                                        eventDate = objectSplit[0].split('"')[1];
                                    }
                                }
                                console.log('I: ', i, ' - Triple: ', triple);
                            }
                            if (debug) {
                                console.log(
                                    "eventID:", eventID,
                                    ", eventType:", eventType,
                                    ", eventLevel:", eventLevel,
                                    ", eventLatitude: ", eventLatitude,
                                    ", eventLongitude: ", eventLongitude,
                                    ", eventDate: ", eventDate);
                            }

                            // var eventIdSplit = triples[0].subject.split('#');
                            // var eventId = eventIdSplit[1];
                            //
                            // var eventTypeSplit = triples[0].object.split('#');
                            // var eventType = eventTypeSplit[1];
                            //
                            // var eventSeveritySplit = triples[2].object.split('^^');
                            // var severityLevel = eventSeveritySplit[0].split('"')[1];
                            //
                            // var eventLatSplit = triples[4].object.split('^^');
                            // var latitude = parseFloat(eventLatSplit[0].split('"')[1]);
                            //
                            // var eventLongSplit = triples[5].object.split('^^');
                            // var longitude = parseFloat(eventLongSplit[0].split('"')[1]);
                            //
                            // var eventDateSplit = triples[8].object.split('^^');
                            // var date = eventDateSplit[0].split('"')[1];
                            //
                            // if (debug) {
                            //     console.log(
                            //         "eventId:", eventId,
                            //         ", eventType:", eventType,
                            //         ", severityLevel:", severityLevel,
                            //         ", latitude: ", latitude,
                            //         ", longitude: ", longitude,
                            //         ", date: ", date);
                            // }
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
