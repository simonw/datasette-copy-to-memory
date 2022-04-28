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


def make_db(db_directory, name):
    db_path = str(db_directory / name)
    db = sqlite_utils.Database(db_path)
    db["test"].insert({"id": 1, "name": "Test"}, pk="id")
    return db_path


@pytest.fixture(scope="session")
def ds(tmp_path_factory):
    db_directory = tmp_path_factory.mktemp("db")
    db_paths = []
    for name in ("test.db", "test2.db"):
        db_paths.append(make_db(db_directory, name))
    return Datasette([db_paths[0]], immutables=[db_paths[1]])


@pytest.mark.asyncio
async def test_copy_to_memory_creates_database(ds):
    # Before init should only be one visible database
    response = await ds.client.get("/-/databases.json")
    names = {r["name"] for r in response.json()}
    assert names == {"test", "test2"}
    await ensure_startup_invoked(ds)
    response2 = await ds.client.get("/-/databases.json")
    names2 = {r["name"] for r in response2.json()}
    assert names2 == {"test", "test_memory", "test2", "test2_memory"}


@pytest.mark.asyncio
@pytest.mark.parametrize("database", ("test", "test_memory", "test2", "test2_memory"))
async def test_copy_to_memory_queries(ds, database):
    await ensure_startup_invoked(ds)
    response = await ds.client.get("/{}/test.json?_shape=array".format(database))
    assert response.json() == [{"id": 1, "name": "Test"}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "metadata,db_names,expected_databases",
    (
        (
            None,
            ("nonetest", "nonetest2"),
            {"nonetest", "nonetest_memory", "nonetest2", "nonetest2_memory"},
        ),
        (
            {"plugins": {"datasette-copy-to-memory": {"databases": ["onetest2"]}}},
            ("onetest", "onetest2"),
            {"onetest", "onetest2", "onetest2_memory"},
        ),
    ),
)
async def test_copy_to_memory_queries(
    tmp_path_factory, metadata, db_names, expected_databases
):
    db_directory = tmp_path_factory.mktemp("db")
    db_paths = []
    for db_name in db_names:
        db_paths.append(make_db(db_directory, db_name))
    ds = Datasette(db_paths, metadata=metadata)
    await ds.invoke_startup()
    response = await ds.client.get("/-/databases.json")
    names = {r["name"] for r in response.json()}
    assert names == expected_databases
