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
# import multiprocessing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.common.variables import route_generator_host, route_generator_port

print route_generator_host + ':' + route_generator_port

bind = route_generator_host + ':' + route_generator_port
# bind = "127.0.0.1:2000"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = "gevent"
backlog = 2048  # Number of requests to keep in the backlog if every worker is busy


def when_ready(server):
    print "\nServer is running..."
