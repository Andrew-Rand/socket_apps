import aiohttp


async def get_status(session: aiohttp.ClientSession, url: str) -> int:
    async with session.get(url) as response:
        return response.status