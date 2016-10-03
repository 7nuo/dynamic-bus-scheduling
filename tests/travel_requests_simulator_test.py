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
from src.data_simulator.travel_requests_simulator import TravelRequestsSimulator
from src.common.logger import log
from src.common.variables import travel_requests_generator_timeout, travel_requests_generator_max_operation_timeout, \
    travel_requests_min_departure_datetime_testing_value, travel_requests_generator_min_number_of_documents, \
    travel_requests_generator_max_number_of_documents
from multiprocessing import Process
import time


class TravelRequestsSimulatorTester(object):
    def __init__(self):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='initialize_travel_requests_simulator: starting')
        self.start_time = time.time()
        self.travel_requests_simulator = TravelRequestsSimulator()
        self.travel_requests_generator_process = None
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='initialize_travel_requests_simulator: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def start_travel_requests_generator_process(self, initial_datetime, min_number_of_travel_request_documents,
                                                max_number_of_travel_request_documents):
        """
        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='travel_requests_generator_process: starting')
        self.travel_requests_generator_process = Process(
            target=self.test_travel_requests_generator_process,
            args=(initial_datetime, min_number_of_travel_request_documents, max_number_of_travel_request_documents)
        )
        self.travel_requests_generator_process.start()

    def terminate_travel_requests_generator_process(self):
        self.travel_requests_generator_process.terminate()
        self.travel_requests_generator_process.join()
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='travel_requests_generator_process: finished')

    def test_clear_travel_requests_collection(self):
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_clear_travel_requests_collection: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.clear_travel_requests_collection()
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_clear_travel_requests_collection: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def test_delete_travel_request_documents(self, object_ids=None, client_ids=None, line_ids=None,
                                             min_departure_datetime=None, max_departure_datetime=None):
        """
        Delete multiple travel_request_documents.

        travel_request_document: {
            '_id', 'client_id', 'line_id',
            'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
            'departure_datetime', 'arrival_datetime',
            'starting_timetable_entry_index', 'ending_timetable_entry_index'
        }
        :param object_ids: [ObjectId]
        :param client_ids: [int]
        :param line_ids: [int]
        :param min_departure_datetime: datetime
        :param max_departure_datetime
        :return: None
        """
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_delete_travel_request_documents: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.delete_travel_request_documents(
            object_ids=object_ids,
            client_ids=client_ids,
            line_ids=line_ids,
            min_departure_datetime=min_departure_datetime,
            max_departure_datetime=max_departure_datetime
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_delete_travel_request_documents: finished - elapsed_time = ' +
                        str(self.elapsed_time) + ' sec')

    def test_generate_random_travel_request_documents(self, initial_datetime, min_number_of_travel_request_documents,
                                                      max_number_of_travel_request_documents):
        """
        Generate random number of travel_request_documents for each bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_generate_random_travel_request_documents: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.generate_random_travel_request_documents(
            initial_datetime=initial_datetime,
            min_number_of_travel_request_documents=min_number_of_travel_request_documents,
            max_number_of_travel_request_documents=max_number_of_travel_request_documents
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_generate_random_travel_request_documents: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_generate_travel_request_documents(self, initial_datetime, number_of_travel_request_documents,
                                               bus_line=None, line_id=None):
        """
        Generate a specific number of travel_request_documents, for the selected bus_line,
        for a 24hour period starting from a selected datetime, and store them at the
        corresponding collection of the System Database.

        bus_line_document: {
            '_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
        }
        :param initial_datetime: datetime
        :param number_of_travel_request_documents: int
        :param bus_line: bus_line_document
        :param line_id: int
        :return: None
        """
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_generate_travel_request_documents: starting')
        self.start_time = time.time()
        self.travel_requests_simulator.generate_travel_request_documents(
            initial_datetime=initial_datetime,
            number_of_travel_request_documents=number_of_travel_request_documents,
            bus_line=bus_line,
            line_id=line_id
        )
        self.elapsed_time = time.time() - self.start_time
        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='test_generate_travel_request_documents: finished - elapsed_time = '
                        + str(self.elapsed_time) + ' sec')

    def test_travel_requests_generator_process(self, initial_datetime, min_number_of_travel_request_documents,
                                               max_number_of_travel_request_documents):
        """
        :param initial_datetime: datetime
        :param min_number_of_travel_request_documents: int
        :param max_number_of_travel_request_documents: int
        :return: None
        """
        time_difference = 0
        initial_time = time.time()

        while time_difference < travel_requests_generator_max_operation_timeout:
            self.test_generate_random_travel_request_documents(
                initial_datetime=initial_datetime,
                min_number_of_travel_request_documents=min_number_of_travel_request_documents,
                max_number_of_travel_request_documents=max_number_of_travel_request_documents
            )
            time.sleep(travel_requests_generator_timeout)
            time_difference = time.time() - initial_time

        log(module_name='travel_requests_simulator_test', log_type='INFO',
            log_message='travel_requests_generator_process: finished')


if __name__ == '__main__':
    travel_requests_simulator_tester = TravelRequestsSimulatorTester()
    # travel_requests_simulator_tester.test_clear_travel_requests_collection()
    #
    # travel_requests_simulator_tester.start_travel_requests_generator_process(
    #     initial_datetime=travel_requests_min_departure_datetime_testing_value,
    #     min_number_of_travel_request_documents=travel_requests_generator_min_number_of_documents,
    #     max_number_of_travel_request_documents=travel_requests_generator_max_number_of_documents
    # )
    #
    # travel_requests_simulator_tester.terminate_travel_requests_generator_process()

