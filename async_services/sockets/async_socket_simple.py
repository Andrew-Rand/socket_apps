"""
    Will be used methods of asyncio event loop for async working with sockets
        connection, address = await loop.sock_accept(socket)  # socket has to be unblocked and already binded to port
        data = await loop.sock_recv(socket)
        sucess = await loop.sock_sendall(socket, data)
"""

import asyncio
import socket


async def tick() -> None:
    """just async sleep"""
    while True:
        await asyncio.sleep(2)
        print('tick')


async def echo(connection: socket.socket, loop: asyncio.AbstractEventLoop) -> None:
    """Process data from connected client and send it back"""
    while data := await loop.sock_recv(connection, 1024):
        print(f'Received {data}')
        await loop.sock_sendall(connection, data)
        print(f'Sent {data}')


async def listen_for_connection(server_socket: socket, loop: asyncio.AbstractEventLoop) -> None:
    """Listening for connections and accepting connections"""
    while True:
        connection, client_address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Client {client_address} connected")
        asyncio.create_task(echo(connection, loop))  # start task to proceess client socke


async def main() -> None:
    # configure socket ----------------------
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.setblocking(False)

    server_socket.bind(('localhost', 8080))
    server_socket.listen()

    print('Ready to accept connections')

    asyncio.create_task(tick())

    await listen_for_connection(server_socket, asyncio.get_event_loop())
    # ---------------------------------------


asyncio.run(main())