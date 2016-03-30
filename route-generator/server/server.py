
class Mutex(object):
    def __init__(self):
        self.val = 0

    def incr(self):
        self.val += 1

mutex = Mutex()


def application(environ, start_response):
    """Simplest possible application object"""
    data = 'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length',  str(len(data)))
    ]
    start_response(status, response_headers)
    changer()
    print mutex.val
    return iter([data])


def changer():
    mutex.incr()
