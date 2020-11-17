#import libraries
import socket
import sys
import io #for environ variables
from datetime import datetime


class WSGIServer(object):

    #set socket information
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a new Socket
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)

        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to address
        listen_socket.bind(server_address)

        # Enable server to accept connections
        listen_socket.listen(self.request_queue_size)

        #Get server host name and port (getsockname returns array with (host, port)
        host = self.listen_socket.getsockname()[0]
        port = self.listen_socket.getsockname()[1]
        self.server_name = socket.getfqdn(host) #e.g. Steffens Thinkpad
        self.server_port = port
        #Return headers set by Web framework
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            #New client connection
            self.client_connection, self.client_address = listen_socket.accept()
            #Handle one request and close the client connection. Then loop over to wait for another client connection
            self.handle_one_request()

    def handle_one_request(self):
        #Read information of incoming Request (e.g. curl -v, GET, POST)
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode("utf-8")
        # Print formatted request data a la 'curl -v'
        print(''.join(
            f'< {line}\n' for line in request_data.splitlines()
        ))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # calls the application (flask) and gets back the HTTP response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, request_data): # gets request_method, path and request_version from recent request
        request_line = request_data.splitlines()[0]
        request_line = request_line.rstrip("\r\n") # Removes all \r\n chars at the end of the string
        # Break down the request line into components
        (self.request_method,  # e.g. GET
        self.path,  # e.g /xxx
        self.request_version  # e.g. HTTP/1.1
        ) = request_line.split()

    def get_environ(self): # gets and returns the environ variables that are necessary for the application (e.g. flask)
        env = {}

        #Required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False

        #Required CGI variables (see parse_request function)
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path  #
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)

        return env


    def start_response(self, status, response_headers, exc_info=None):

        # Add necessary server headers -> message send to app
        server_headers = [
            ('Date', str(datetime.now())),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data a la 'curl -v'
            print(''.join(
                f'> {line}\n' for line in response.splitlines()
            ))
            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()



def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


#Set HOST and PORT (first argument is HOST, 2nd is PORT)
HOST = sys.argv[1]
PORT = int(sys.argv[2])
SERVER_ADDRESS = (HOST, PORT)

#Hard coded the module that will be started by the WSGI Server
module = "flaskapp" #Name of the .py file containing the flask data
application = "app" #Name of the app specified in the module

if __name__ == '__main__':
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()