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

var MongoClient = require('mongodb').MongoClient;
var mongodbHost = '127.0.0.1';
var mongodbPort = '27017';
var mongodbDatabaseName = 'monad';
var url = 'mongodb://' + mongodbHost + ':' + mongodbPort + '/' + mongodbDatabaseName;
var mongodbDatabase = null;
var trafficEventsCollection = null;

function deleteTrafficEventDocument(eventId) {
    var key = {
        "event_id": eventId.toString()
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

function establishConnection() {
    MongoClient.connect(url, function(err, db) {
        if (err) {
            console.error('mongodb_database_connection: establishConnection:', err.message);
        }
        else {
            console.log('mongodb_database_connection: establishConnection: ok');
            mongodbDatabase = db;
            whenConnected();
        }
    });
}

function findTrafficEventDocument(eventId) {
    var trafficEventDocument = null;
    var key = {
        "event_id": eventId.toString()
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

function insertTrafficEventDocument(eventId, eventType, severityLevel, latitude, longitude, date) {
    var key = {
        "event_id": eventId.toString()
    };
    var data = {$set: {
        "event_type": eventType,
        "severity_level": severityLevel,
        "latitude": latitude,
        "longitude": longitude,
        "date": date
    }};
    trafficEventsCollection.updateOne(key, data, {upsert:true},  function (err, result) {
        if (err) {
            console.error('mongodb_database_connection: insertTrafficEventDocument:', err.message);
        }
    });
}

function whenConnected() {
    trafficEventsCollection = mongodbDatabase.collection('TrafficEvents');
    // insertTrafficEventDocument(
    //     eventId=1,
    //     eventType=1,
    //     severityLevel=1,
    //     latitude=1,
    //     longitude=1,
    //     date=1
    // );
    // findTrafficEventDocument(eventId=1);
    // deleteTrafficEventDocument(eventId=1);
    // findTrafficEventDocument(eventId=1);
    mongodbDatabase.close();
}

establishConnection();

