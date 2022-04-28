from datasette import hookimpl


@hookimpl
def startup(datasette):
    async def inner():
        for db in datasette.databases.values():
            if db.path:
                memory_name = "{}_memory".format(db.name)
                memory_db = datasette.add_memory_database(memory_name)
                # Ensure the in-memory database is initalized
                await memory_db.execute("select 1 + 1")

                def vacuum_into(conn):
                    conn.execute(
                        "VACUUM INTO ?",
                        ["file:{}?mode=memory&cache=shared".format(memory_name)],
                    )

                await db.execute_write_fn(vacuum_into)

    return inner
