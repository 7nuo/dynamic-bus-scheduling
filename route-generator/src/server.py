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


class MyEncoder(json.JSONEncoder):
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
        if path_info == '/get_bus_stops':
            bus_stops = mongo.get_bus_stops_dictionary_to_list()
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(bus_stops)

        elif path_info == '/get_route_between_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
            starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
            ending_bus_stop_name = form.getvalue('ending_bus_stop_name')

            route = mongo.get_route_between_bus_stops(starting_bus_stop_name=starting_bus_stop_name,
                                                      ending_bus_stop_name=ending_bus_stop_name)
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(route, cls=MyEncoder)

        elif path_info == '/get_multiple_routes_between_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
            starting_bus_stop_name = form.getvalue('starting_bus_stop_name')
            ending_bus_stop_name = form.getvalue('ending_bus_stop_name')

            routes = mongo.get_multiple_routes_between_bus_stops(starting_bus_stop_name=starting_bus_stop_name,
                                                                 ending_bus_stop_name=ending_bus_stop_name)
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(routes, cls=MyEncoder)

        elif path_info == '/get_route_between_multiple_bus_stops':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
            bus_stop_names = form.getvalue('bus_stop_names')
            intermediate_routes = mongo.get_route_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
            response_status = '200 OK'
            response_type = 'application/json'
            response = json.dumps(intermediate_routes, cls=MyEncoder)

    response_headers = [
        ('Content-Type', response_type),
        ('Content-Length', str(len(response)))
    ]

    start_response(response_status, response_headers)
    return [response]
