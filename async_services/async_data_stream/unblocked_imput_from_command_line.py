import asyncio
from asyncio import StreamReader
import sys
import tty


"""
Warning
If input in the same time with output, the app will work incorrectly.
"""

async def create_stdin_reader() -> StreamReader:
    """Use to create async input"""

    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)  # connect protocol to file like object (stdin from system here)

    return stream_reader


async def delay(sec: int):
    print(f'Sleeping {sec} seconds...')
    await asyncio.sleep(sec)
    print(f'Done {sec} seconds')


async def main():
    stdin_reader: StreamReader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))


asyncio.run(main())
