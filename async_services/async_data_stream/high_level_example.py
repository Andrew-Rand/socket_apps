import asyncio
import typing


async def read_until_empty(stream_reader: asyncio.StreamReader) -> typing.AsyncGenerator[str, None]:
    """Read and decode until the end of the symbols"""
    while response := await stream_reader.readline():
        yield response.decode()


async def main():
    host: str = 'www.example.com'
    request: str = f"GET / HTTP/1.1\r\r" \
                   f"Connection: close\r\n"\
                   f"Host: {host}\r\n\r\n"

    stream_reader, stream_writer = await asyncio.open_connection(host, 80)

    try:
        stream_writer.write(request.encode())
        await stream_writer.drain()  # drain guarantee all data were sent
        while True:

            print(await anext(read_until_empty(stream_reader)))

        # responses = [response async for response in read_until_empty(stream_reader)]
        # print(''.join(responses))

    finally:
        stream_writer.close()


asyncio.run(main())

