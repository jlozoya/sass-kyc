import asyncio
from app.core.db import get_database


async def run():
    db = get_database()
    print(await db.list_collection_names())


asyncio.run(run())
