"""
Using handmade event loop and OS notification system
"""


import selectors  # API to use OS notifications
import socket

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.setblocking(False)  # do not block on methods recv and acept
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)  # register socket as event

while True:
    events: list[tuple[selectors.SelectorKey, int]] = selector.select(timeout=3) # collect events with timeout (if timeout, return empty list)

    if len(events) == 0:
        print('No events, waiting...')  # in case of timeout
        continue

    for event, _ in events:
        event_socket = event.fileobj  # get socket of this event
        if event_socket == server_socket:  # if event happend with sever socket - this is a connection from client
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f'Connection from {address}')
            selector.register(connection, selectors.EVENT_READ) # also register client socket in event system
        else:
            # if event not of server socket - this is a client socket
            data = event_socket.recv(1024)
            print(f'Received data {data}')
            event_socket.send(data) # send data back to socket


