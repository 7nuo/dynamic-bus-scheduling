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
import cgi
import json

from router import Router


router = Router()


class JSONResponseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def application(env, start_response):
    data_env = env.copy()
    method = data_env.get('REQUEST_METHOD')
    path_info = data_env.get('PATH_INFO')

    if method != 'POST':
        response_status = '500 INTERNAL ERROR'
        response_type = 'plain/text'
        response = 'ERROR'
    else:
        if path_info == '/get_route_between_two_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)

            starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
            ending_bus_stop_name = form.getvalue('ending_bus_stop_name')
            result = router.get_route_between_two_bus_stops(starting_bus_stop_name=starting_bus_stop_name,
                                                            ending_bus_stop_name=ending_bus_stop_name)
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(result, cls=JSONResponseEncoder)

        elif path_info == '/get_route_between_multiple_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)

            bus_stop_names = form.getvalue('bus_stop_names')
            result = router.get_route_between_multiple_bus_stops(bus_stop_names=bus_stop_names)

            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(result, cls=JSONResponseEncoder)

        elif path_info == '/get_waypoints_between_two_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)

            starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
            ending_bus_stop_name = form.getvalue('ending_bus_stop_name')
            result = router.get_waypoints_between_two_bus_stops(starting_bus_stop_name=starting_bus_stop_name,
                                                                ending_bus_stop_name=ending_bus_stop_name)
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(result, cls=JSONResponseEncoder)

        elif path_info == '/get_waypoints_between_multiple_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)

            bus_stop_names = form.getvalue('bus_stop_names')
            result = router.get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)

            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(result, cls=JSONResponseEncoder)

        # elif path_info == '/get_multiple_routes_between_bus_stops':
        #     form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
        #     starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
        #     ending_bus_stop_name = form.getvalue('ending_bus_stop_name')
        #     number_of_routes = int(form.getvalue('number_of_routes'))
        #
        #     result = router.get_multiple_routes_between_bus_stops(starting_bus_stop_name=starting_bus_stop_name,
        #                                                           ending_bus_stop_name=ending_bus_stop_name,
        #                                                           number_of_routes=number_of_routes)
        #     response_status = '200 OK'
        #     response_type = 'application/json'
        #     response = json.dumps(result, cls=JSONResponseEncoder)

        # elif path_info == '/get_multiple_routes_between_multiple_bus_stops':
        #     form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
        #
        #     bus_stop_names = form.getvalue('bus_stop_names')
        #     number_of_routes = int(form.getvalue('number_of_routes'))
        #     result = router.get_multiple_routes_between__multiple_bus_stops(bus_stop_names=bus_stop_names,
        #                                                                     number_of_routes=number_of_routes)
        #     response_status = '200 OK'
        #     response_type = 'application/json'
        #     response = json.dumps(result, cls=JSONResponseEncoder)

        else:
            response_status = '500 INTERNAL ERROR'
            response_type = 'plain/text'
            response = 'ERROR'

    response_headers = [
        ('Content-Type', response_type),
        ('Content-Length', str(len(response)))
    ]

    start_response(response_status, response_headers)
    return [response]
