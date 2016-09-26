// Copyright 2016 Eleftherios Anagnostopoulos for Ericsson AB
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not use
// this file except in compliance with the License. You may obtain a copy of the
// License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

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

