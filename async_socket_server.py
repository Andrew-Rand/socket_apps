"""
    Will be used methods of asyncio event loop for async working with sockets
        connection, address = await loop.sock_accept(socket)  # socket has to be unblocked and already binded to port
        data = await loop.sock_recv(socket)
        sucess = await loop.sock_sendall(socket, data)
"""

