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
from src.osm_parser.osm_parser import OsmParser
from src.common.logger import log
from src.common.variables import testing_osm_filename


class OsmParserTester(object):
    def __init__(self, osm_filename):
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='initialize_osm_parser: starting')
        self.start_time = time.time()
        self.osm_parser = OsmParser(osm_filename=osm_filename)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='initialize_osm_parser: finished - elapsed time = '
                        + str(self.elapsed_time) + ' sec')

    def test_parse_osm_file(self):
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='test_parse_osm_file: starting')
        self.start_time = time.time()
        self.osm_parser.parse_osm_file()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='test_parse_osm_file: finished - elapsed time = '
                        + str(self.elapsed_time) + ' sec')

    def test_populate_all_collections(self):
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='test_populate_all_collections: starting')
        self.start_time = time.time()
        self.osm_parser.populate_all_collections()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser_test', log_type='INFO',
            log_message='test_populate_all_collections: finished - elapsed time = ' +
                        str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    tester = OsmParserTester(osm_filename=os.path.join(os.path.dirname(__file__), testing_osm_filename))
    # travel_requests_simulator_tester.test_parse_osm_file()
    # travel_requests_simulator_tester.test_populate_all_collections()
