from pymilvus import connections, utility, Collection
from setting import SCHEMA, FIELD2INDEX_PARAMS


def create_milvus_collection(name: str = "test"):
    connections.connect("default")
    if utility.has_collection(name):
        connections.disconnect("default")
        raise Exception(f"Collection {name} already exists.")
    collection = Collection(name, SCHEMA)

    for field, index_params in FIELD2INDEX_PARAMS.items():
        collection.create_index(field, index_params)

    connections.disconnect("default")


def drop_milvus_collection(name: str = "test"):
    connections.connect("default")
    utility.drop_collection(name)
    connections.disconnect("default")
