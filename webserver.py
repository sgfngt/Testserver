#import libraries
import socket

#Init HOST and PORT
HOST = ""
PORT = 8888

#Create a new Socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Bind the socket to address
listen_socket.bind((HOST, PORT))
#Enable server to accept connections
listen_socket.listen(1)

print("Serving HTTP on port "+str(PORT))

while True:
    client_connection, client_address = listen_socket.accept()
    #get information of client connection
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))

    #define response
    http_response = b"""\
HTTP/1.1 200 OK

Allah ist gross
"""
    #send response
    client_connection.sendall(http_response)
    client_connection.close()
