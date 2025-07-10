import asyncio
from asyncio.subprocess import Process


async def main():
    process: Process = await asyncio.create_subprocess_exec('sleep', '3')
    print(f'Process pid {process.pid}')
    try:
        status_code = await asyncio.wait_for(process.wait(), timeout=1.0)
        print(f'Process exit code {status_code}')
    except asyncio.TimeoutError:
        print(f'Process timed out, killing process')
        process.terminate()
        status_code = await process.wait()
        print(f'Process exit code {status_code}')


asyncio.run(main())