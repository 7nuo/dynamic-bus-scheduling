#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Copyright 2016 Eleftherios Anagnostopoulos for Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from src.mongodb_database.mongo_connection import MongoConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
import random


class TravelRequestsSimulator(object):
    def __init__(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='travel_requests_simulator', log_type='DEBUG', log_message='mongodb_database connection ok')

    def generate_travel_requests(self):
        weighted_choices = [('Red', 1), ('Blue', 2)]
        population = [val for val, cnt in weighted_choices for i in range(cnt)]
        rc = 0
        bc = 0

        for i in range(0, 100000):
            x = random.choice(population)
            if x == 'Red':
                rc += 1
            else:
                bc += 1

        print rc, bc
