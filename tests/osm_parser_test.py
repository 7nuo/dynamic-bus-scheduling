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


class OSMParserTester(object):
    def __init__(self, osm_filename):
        log(module_name='osm_parser', log_type='INFO', log_message='init: starting')
        self.start_time = time.time()
        self.parser = Parser(osm_filename=osm_filename)
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser', log_type='INFO',
            log_message='init: finished - elapsed time = ' + str(self.elapsed_time) + ' sec')

    def parse(self):
        log(module_name='osm_parser', log_type='INFO', log_message='parse: starting')
        self.start_time = time.time()
        self.parser.parse()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser', log_type='INFO',
            log_message='parse: finished - elapsed time = ' + str(self.elapsed_time) + ' sec')

    def populate_all_collections(self):
        log(module_name='osm_parser', log_type='INFO', log_message='populate_all_collections: starting')
        self.start_time = time.time()
        self.parser.populate_all_collections()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='osm_parser', log_type='INFO',
            log_message='populate_all_collections: finished - elapsed time = ' +
                        str(self.elapsed_time) + ' sec')


if __name__ == '__main__':
    tester = OSMParserTester(osm_filename=os.path.join(os.path.dirname(__file__),
                                                       '../resources/osm_files/uppsala.osm'))
    # tester.parse()
    # tester.populate_all_collections()
