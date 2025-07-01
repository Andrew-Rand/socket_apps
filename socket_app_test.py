import asyncio
import socket

# simple blocked socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ip + port, TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to avoid socket already in use error

address = ('127.0.0.1', 8000)
server_socket.bind(address)

server_socket.listen()  # listen requests from clients

print('Waiting for connection...')

try:
    connection, client_address = server_socket.accept() # wait until client connected, connection - is a socket connected with client
    print('Connection from', client_address)

    buffer = b''

    while buffer[-2:] != b'\r\n':  # enter in telnet terminal
        data = connection.recv(2) # get 2 bytes from client
        if not data:
            break
        else:
            print('Received', data)
            buffer += data

    print('All data', buffer)

    connection.sendall(buffer) # send all data back to client socket

finally:
    server_socket.close()  # close server socket

# you can connect in terminal with
# telnet localhost 8000

