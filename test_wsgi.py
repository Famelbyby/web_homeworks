from urllib.parse import parse_qs, urlparse

HELLO_WORLD = b"Hello world!\n"


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    d = parse_qs(environ['QUERY_STRING'])
    print('Query string: ')
    for k in d:
        print(k, ' = ', d[k][0])
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    print('Post parameters: ')
    for k in d:
        print(k.decode('utf-8'), ' = ', d[k][0].decode('utf-8'))
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


application = simple_app


class AppClass:
    """Produce the same output, but using a class

    (Note: 'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
