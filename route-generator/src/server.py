import cgi
import json
import os
# import parser

# import serverConfig
# from connection_handler import MongoConnector
from mongo_connector import MongoConnector
from path_finder import find_path, find_multiple_paths

HOST = '127.0.0.1'
PORT = 27017
mongo = MongoConnector(host=HOST, port=PORT)


def application(env, start_response):
    data_env = env.copy()
    method = data_env.get('REQUEST_METHOD')
    path_info = data_env.get('PATH_INFO')

    if method != 'POST':
        response_status = '500 INTERNAL ERROR'
        response_type = 'plain/text'
        response = 'ERROR'
    else:
        if path_info == '/get_bus_stops':
            bus_stops = mongo.get_bus_stops()
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(bus_stops)

        elif path_info == '/get_route_between_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
            starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
            ending_bus_stop_name = form.getvalue('ending_bus_stop_name')

            route = mongo.get_route_from_bus_stop_names(starting_bus_stop_name=starting_bus_stop_name,
                                                        ending_bus_stop_name=ending_bus_stop_name)
            response_status = '200 OK'
            response_type = 'text/plain'
            response = str(route)

    response_headers = [
        ('Content-Type', response_type),
        ('Content-Length', str(len(response)))
    ]

    start_response(response_status, response_headers)
    return [response]
