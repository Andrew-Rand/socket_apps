from threading import Thread
import socket


class CustomEchoThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    # if no data - closed by client or stopped by server
                    raise BrokenPipeError('Connection closed by remote host')
                print(f'Received {data}')
                self.client.send_all(data)
        except OSError as e:
            # in case of exception interrupt run method, the thread will stopped
            print(f'Thread was interrupted by error: {e}')

    def close(self):
        if self.is_alive():
            # if thread os still active (if client closed connection)
            self.client.send_all(bytes('Stopping', encoding='utf-8'))
            self.client.shutdown(socket.SHUT_RDWR)  # stop read and write, break client connection


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen()
    connection_threads = []

    try:
        while True:
            connection, address = server.accept()
            thread = CustomEchoThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        # in case of keyboard interrupt close all connetions
        print('Shutting down')
        [thread.close() for thread in connection_threads]