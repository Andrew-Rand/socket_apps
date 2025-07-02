import asyncio
import typing
import uuid
from random import sample

import asyncpg


def generate_brand_names() -> list[tuple]:
    return [(uuid.uuid4().hex,) for _ in range(100)]

async def insert_brands(connection) -> int:
    brands = generate_brand_names()
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)

async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='products',
        password='password',
    )
    await insert_brands(connection)

asyncio.run(main())