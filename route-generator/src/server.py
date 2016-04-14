import cgi
import json
import os
# import parser

# import serverConfig
# from connection_handler import MongoConnector


def application(env, start_response):
    data_env = env.copy()
    method = data_env.get('REQUEST_METHOD')
    path_info = data_env.get('PATH_INFO')

    if method != 'POST':
        response = 'ERROR'
    else:
        if path_info == '/get_route':
            form = cgi.FieldStorage(fp=env['wsgi.input'], environ=data_env)
            starting_point = form.getvalue('starting_point')
            print str(float(starting_point[0]) + 2.0)
            print os.path.dirname(os.path.realpath(__file__))
            # response = str(serverConfig.mongo.list_of_bus_stops)
            response = 'OK\n'

    response_status = '200 OK'
    response_type = 'text/plain'

    # mongo = MongoConnector(parser=None, host='127.0.0.1', port=27017)

    # print str(serverConfig.mongo.list_of_bus_stops)

    response_headers = [
        ('Content-Type', response_type),
        ('Content-Length', str(len(response)))
    ]

    start_response(response_status, response_headers)
    return response
