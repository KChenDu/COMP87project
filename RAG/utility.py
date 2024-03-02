import sqlite3

from pymilvus import connections, utility, Collection
from setting import SCHEMA, FIELD2INDEX_PARAMS
from loguru import logger
from pathlib import Path
from sqlite3 import Error


def create_milvus_collection(name: str = "test"):
    connections.connect("default")
    if utility.has_collection(name):
        connections.disconnect("default")
        raise Exception("Collection <" + name + "> already exists.")
    collection = Collection(name, SCHEMA)

    for field, index_params in FIELD2INDEX_PARAMS.items():
        collection.create_index(field, index_params)

    connections.disconnect("default")
    logger.info("Collection <" + name + "> created")


def milvus_collection_exists(name: str = "test") -> bool:
    connections.connect("default")
    result = utility.has_collection(name)
    connections.disconnect("default")
    return result


def drop_milvus_collection(name: str = "test"):
    connections.connect("default")
    if not utility.has_collection(name):
        connections.disconnect("default")
        raise Exception("Collection <" + name + "> does not exist.")
    logger.info("Dropping collection <" + name + '>')
    utility.drop_collection(name)
    connections.disconnect("default")
    logger.info("Collection <" + name + "> dropped")


def create_sqlite_db(name: str = "test"):
    """ create a database connection to a SQLite database """
    db_file = Path("sqlite/" + name + ".db")
    if db_file.is_file():
        raise Exception("Database <" + name + "> already exists.")
    try:
        conn = sqlite3.connect(db_file)
        conn.close()
    except Error as e:
        raise Exception(e)
    logger.info("Database <" + name + "> created")


def sqlite_db_exists(name: str = "test") -> bool:
    db_file = Path("sqlite/" + name + ".db")
    return db_file.is_file()


def drop_sqlite_db(name: str = "test"):
    """ drop a SQLite database """
    db_file = Path("sqlite/" + name + ".db")
    if not db_file.is_file():
        raise Exception("Database <" + name + "> does not exist.")
    logger.info("Dropping database <" + name + '>')
    Path.unlink(db_file)
    logger.info("Database <" + name + "> dropped")