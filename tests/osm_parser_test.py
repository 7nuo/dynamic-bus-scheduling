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
from src.common.parameters import testing_osm_filename

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class OsmParserTester(object):
    def __init__(self, osm_filename):
        self.module_name = 'osm_parser_tester'
        self.log_type = 'INFO'
        self.log_message = 'initialize_osm_parser: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.osm_parser = OsmParser(osm_filename=osm_filename)
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'initialize_osm_parser: finished - elapsed time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_parse_osm_file(self):
        self.log_message = 'test_parse_osm_file: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.osm_parser.parse_osm_file()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_parse_osm_file: finished - elapsed time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

    def test_populate_all_collections(self):
        self.log_message = 'test_populate_all_collections: starting'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)

        self.start_time = time.time()
        self.osm_parser.populate_all_collections()
        self.elapsed_time = time.time() - self.start_time

        self.log_message = 'test_populate_all_collections: finished - elapsed time = ' \
                           + str(self.elapsed_time) + ' sec'
        log(module_name=self.module_name, log_type=self.log_type, log_message=self.log_message)


if __name__ == '__main__':
    osm_parser_tester = OsmParserTester(
        osm_filename=os.path.join(os.path.dirname(__file__), testing_osm_filename)
    )
    while True:
        time.sleep(0.01)
        selection = raw_input(
            '\n0.  exit'
            '\n1.  test_parse_osm_file'
            '\n2.  test_populate_all_collections'
            '\nSelection: '
        )
        # 0. exit
        if selection == '0':
            break

        # 1. test_parse_osm_file
        elif selection == '1':
            osm_parser_tester.test_parse_osm_file()

        # 2. test_populate_all_collections
        elif selection == '2':
            osm_parser_tester.test_populate_all_collections()

        else:
            pass
