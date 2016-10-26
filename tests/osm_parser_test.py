#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2016 Eleftherios Anagnostopoulos for Ericsson AB (EU FP7 CityPulse Project)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.osm_parser.osm_parser import OsmParser
from src.common.logger import log
from src.common.variables import testing_osm_filename

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


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
