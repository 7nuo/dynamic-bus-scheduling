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
import os
import time
from src.osm_parser.parser import Parser
from src.common.logger import log


if __name__ == '__main__':
    osm_filename = os.path.join(os.path.dirname(__file__), '../resources/osm_files/uppsala.osm')
    parser = Parser(osm_filename=osm_filename)

    log(module_name='osm_parser', log_type='INFO', log_message='parse: starting')
    start_time = time.time()
    parser.parse()
    elapsed_time = time.time() - start_time
    log(module_name='osm_parser', log_type='INFO',
        log_message='parse: finished - elapsed time = ' + str(elapsed_time) + ' sec')

    log(module_name='osm_parser', log_type='INFO', log_message='populate_all_collections: starting')
    start_time = time.time()
    parser.populate_all_collections()
    elapsed_time = time.time() - start_time
    log(module_name='osm_parser', log_type='INFO',
        log_message='populate_all_collections: finished - elapsed time = ' + str(elapsed_time) + ' sec')
