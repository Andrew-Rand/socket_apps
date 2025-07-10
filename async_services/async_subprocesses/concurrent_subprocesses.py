import asyncio
import random
import string
import time


async def encrypt(text: str) -> bytes:
    cmd = ['gpg', '-c', '--batch', '--passphrase', '3ncryptm3', '--cipher-algo', 'TWOFISH']  # code the text
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,  # input control, new stream
        stdout=asyncio.subprocess.PIPE,  # output control, new stream
    )
    stdout, stderr = await process.communicate(input=text.encode())  # communicate with stream created above

    return stdout

async def main():
    text_list = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    s = time.time()
    tasks = [asyncio.create_task(encrypt(text)) for text in text_list]
    encrypted = await asyncio.gather(*tasks)
    e = time.time()
    print(f'working time {e - s}')
    print(encrypted)


asyncio.run(main())