from threading import Thread
import socket


def echo(client: socket.socket):
    while True:
        data = client.recv(1024)
        print(f'Received data: {data}')
        client.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen()
    while True:
        connection, _ = server.accept()  # blocked before connection
        thread = Thread(target=echo, args=(connection,))  # process client in thread
        thread.daemon = True  # if you need to close application regardless of running threads
        thread.start()
