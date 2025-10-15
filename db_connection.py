import asyncpg

db_configs = {
    "5432": dict(user='postgres', password='postgres', database='postgres', host='127.0.0.1', port=5432),
    "5433": dict(user='postgres', password='postgres', database='postgres', host='127.0.0.1', port=5433),
    "5434": dict(user='postgres', password='postgres', database='postgres', host='127.0.0.1', port=5434),
}



def get_db_connector() -> callable:
    connection_cache: dict[str, asyncpg.Connection] = {}

    async def connector(port: str) -> asyncpg.Connection:
        # Create or reuse connection
        conn = connection_cache.get(port)
        if not conn or conn.is_closed():
            conn = await asyncpg.connect(**db_configs[port])
            connection_cache[port] = conn

        return conn

    return connector
