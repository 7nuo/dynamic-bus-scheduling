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

var N3 = require('n3');
var amqp = require('amqplib/callback_api');
var amqpEndpoint = 'amqp://localhost:8007/';
var amqpConnection = null;

var queueName = 'dynamic-bus-scheduling';
// exchanges: 'annotated_data', 'events'
var exchange = 'events';
// routingKeys: '#', 'Aarhus.Road.Traffic.195070', 'Aarhus.Road.Traffic.201345'
var routingKey = '#';
var trafficEventsSource = 'http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam';

var MongoClient = require('mongodb').MongoClient;
var mongodbHost = '127.0.0.1';
var mongodbPort = '27017';
var mongodbDatabaseName = 'dynamic_bus_scheduling';
var url = 'mongodb://' + mongodbHost + ':' + mongodbPort + '/' + mongodbDatabaseName;
var mongodbDatabase = null;
var trafficEventsCollection = null;

var addToDatabase = true;
var debug = true;

function establishConnections() {
    establishMongodbDatabaseConnection();
    establishCityPulseDataBusConnection();
}

function establishMongodbDatabaseConnection() {
    MongoClient.connect(url, function(err, db) {
        if (err) {
            console.error('mongodb_database_connection: establishConnection:', err.message);
        }
        else {
            console.log('mongodb_database_connection: establishConnection: ok');
            mongodbDatabase = db;
            whenConnectedToMongodbDatabase();
        }
    });
}

function establishCityPulseDataBusConnection() {
    amqp.connect(amqpEndpoint, function(err, conn) {
        if (err) {
            console.error('citypulse_data_bus_connection: error', err.message);
            return setTimeout(establishCityPulseDataBusConnection, 1000);
        }
        conn.on('error', function(err) {
            if (err.message !== 'Connection closing') {
                console.error('citypulse_data_bus_connection: error', err.message);
            }
        });
        conn.on('close', function() {
            console.error('citypulse_data_bus_connection: reconnecting');
            return setTimeout(establishCityPulseDataBusConnection, 1000);
        });
        console.log('citypulse_data_bus_connection: connected');
        amqpConnection = conn;
        whenConnectedToCityPulseDataBus();
    });
}

// Example of traffic jam event:
//
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
    var ok = amqpConnection.createChannel(on_open);

    function on_open(err, ch) {
        if (err != null) {
            console.error(err.message);
        }
        ch.assertQueue(queueName, {
            'messageTtl': 600000,
            'autoDelete': true,
            'durable': false
        });
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

                        if (triple.object.toString() == trafficEventsSource) {
                            trafficJam = true;
                        }
                    }
                    else {
                        if (trafficJam) {
                            var objectSplit, eventID, eventType, eventLevel, eventLatitude, eventLongitude,
                                eventDatetime;
                            console.log(triples);

                            for (var i = 0; i < triples.length; i++) {
                                triple = triples[i];

                                // subject: 'http://purl.oclc.org/NET/UNIS/sao/sao#cc5fe3f9-2a52-4134-a85b-9b2990918abd'
                                // predicate: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
                                // object: 'http://purl.oclc.org/NET/UNIS/sao/ec#TrafficJam'
                                if (triple.object.toString() == trafficEventsSource) {
                                    var subjectSplit = triple.subject.split('#');
                                    eventID = subjectSplit[1];
                                    eventType = 'TrafficJam';
                                }
                                else {
                                    var predicateEnding = triple.predicate.split('#')[1];

                                    // predicate: 'http://purl.oclc.org/NET/UNIS/sao/sao#hasLevel'
                                    // object: '"2"^^http://www.w3.org/2001/XMLSchema#long'
                                    if (predicateEnding == 'hasLevel') {
                                        objectSplit = triple.object.split('^^');
                                        eventLevel = objectSplit[0].split('"')[1];
                                    }
                                    // predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lat'
                                    // object: '"56.1155615424"^^http://www.w3.org/2001/XMLSchema#double'
                                    else if (predicateEnding == 'lat') {
                                        objectSplit = triple.object.split('^^');
                                        eventLatitude = parseFloat(objectSplit[0].split('"')[1]);
                                    }
                                    // predicate: 'http://www.w3.org/2003/01/geo/wgs84_pos#lon'
                                    // object: '"10.1870405674"^^http://www.w3.org/2001/XMLSchema#double'
                                    else if (predicateEnding == 'lon') {
                                        objectSplit = triple.object.split('^^');
                                        eventLongitude = parseFloat(objectSplit[0].split('"')[1]);
                                    }
                                    // predicate: 'http://purl.org/NET/c4dm/timeline.owl#time'
                                    // object: '"2016-10-11T11:13:21.000Z"^^http://www.w3.org/2001/XMLSchema#dateTime'
                                    else if (predicateEnding == 'time') {
                                        objectSplit = triple.object.split('^^');
                                        eventDatetime = objectSplit[0].split('"')[1];
                                    }
                                }
                                // console.log('I: ', i, ' - Triple: ', triple);
                            }
                            if (debug) {
                                console.log(
                                    'eventID:', eventID,
                                    ', eventType:', eventType,
                                    ', eventLevel:', eventLevel,
                                    ', eventLatitude: ', eventLatitude,
                                    ', eventLongitude: ', eventLongitude,
                                    ', eventDatetime: ', eventDatetime);
                            }
                            if (addToDatabase) {
                                insertTrafficEventDocument(
                                    eventID, eventType, eventLevel, eventLatitude, eventLongitude, eventDatetime
                                );
                            }
                        }
                    }
                });
            }
        });
    }
}

function deleteTrafficEventDocument(eventId) {
    var key = {
        'event_id': eventId.toString()
    };
    trafficEventsCollection.deleteOne(key, function (err, result) {
        if (err) {
            console.error('mongodb_database_connection: deleteTrafficEventDocument:', err.message);
        }
        else {
            console.log('mongodb_database_connection: deleteTrafficEventDocument:', result.deletedCount);
        }
    });
}

function findTrafficEventDocument(eventId) {
    var trafficEventDocument = null;
    var key = {
        'event_id': eventId.toString()
    };
    trafficEventsCollection.findOne(key, function (err, result) {
        if (err) {
            console.error('mongodb_database_connection: findTrafficEventDocument:', err.message);
        }
        else {
            trafficEventDocument = result;
        }
    });
    return trafficEventDocument;
}

function insertTrafficEventDocument(eventId, eventType, eventLevel, eventLatitude, eventLongitude, eventDatetime) {
    var key = {
        'event_id': eventId.toString()
    };
    var data = {$set: {
        'event_type': eventType,
        'event_level': eventLevel,
        'point': {'longitude': eventLongitude, 'latitude': eventLatitude},
        'datetime': eventDatetime
    }};
    trafficEventsCollection.updateOne(key, data, {upsert:true},  function (err, result) {
        if (err) {
            console.error('mongodb_database_connection: insertTrafficEventDocument:', err.message);
        }
    });
}

function whenConnectedToMongodbDatabase() {
    trafficEventsCollection = mongodbDatabase.collection('TrafficEventDocuments');
    // mongodbDatabase.close();
}

function whenConnectedToCityPulseDataBus() {
    consumer();
}

establishConnections();
