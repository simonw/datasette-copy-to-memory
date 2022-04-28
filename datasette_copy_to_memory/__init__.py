from datasette import hookimpl
from datasette.utils import sqlite3


@hookimpl
def startup(datasette):
    plugin_config = datasette.plugin_config("datasette-copy-to-memory") or {}
    databases = plugin_config.get("databases")

    async def inner():
        for db in datasette.databases.values():
            if databases:
                if db.name not in databases:
                    continue
            if db.path:
                memory_name = "{}_memory".format(db.name)
                datasette.add_memory_database(memory_name)
                # Use a different in-memory database to co-ordinate the VACUUM INTO
                tmp = sqlite3.connect(":memory:", uri=True)
                tmp.execute("ATTACH DATABASE ? AS _copy_from", [db.path])
                tmp.execute(
                    "VACUUM _copy_from INTO ?",
                    ["file:{}?mode=memory&cache=shared".format(memory_name)],
                )

    return inner
