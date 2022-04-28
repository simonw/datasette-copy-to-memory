from re import S
from datasette.app import Datasette
import pytest
import sqlite_utils

# Running invoke_startup() twice causes a MemoryError
startup_invoked = False


async def ensure_startup_invoked(ds):
    global startup_invoked
    if not startup_invoked:
        await ds.invoke_startup()
        startup_invoked = True


@pytest.fixture(scope="session")
def ds(tmp_path_factory):
    db_directory = tmp_path_factory.mktemp("db")
    db_path = str(db_directory / "test.db")
    db = sqlite_utils.Database(db_path)
    db["test"].insert({"id": 1, "name": "Test"}, pk="id")
    return Datasette([db_path], metadata={})


@pytest.mark.asyncio
async def test_copy_to_memory_creates_database(ds):
    # Before init should only be one visible database
    response = await ds.client.get("/-/databases.json")
    names = [r["name"] for r in response.json()]
    assert names == ["test"]
    await ensure_startup_invoked(ds)
    response2 = await ds.client.get("/-/databases.json")
    names2 = [r["name"] for r in response2.json()]
    assert set(names2) == {"test", "test_memory"}


@pytest.mark.asyncio
@pytest.mark.parametrize("database", ("test", "test_memory"))
async def test_copy_to_memory_queries(ds, database):
    await ensure_startup_invoked(ds)
    response = await ds.client.get("/{}/test.json?_shape=array".format(database))
    assert response.json() == [{"id": 1, "name": "Test"}]
