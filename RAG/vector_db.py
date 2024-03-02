from pymilvus import connections, utility, Collection
from utility import milvus_collection_exists
from loguru import logger


class MilvusCollection:
    def __init__(self, name: str = "test"):
        if not milvus_collection_exists(name):
            raise Exception(f"Collection " + name + " does not exist.")
        self.__collection_name = name

    def switch_to_collection(self, name: str):
        if not milvus_collection_exists(name):
            raise Exception(f"Collection " + name + " does not exist.")
        self.__collection_name = name

    def create_partition(self, partition_name: str, description: str = ""):
        connections.connect("default")
        collection_name = self.__collection_name
        Collection(collection_name).create_partition(partition_name, description)
        logger.info("Partition <" + partition_name + "> created in collection <" + collection_name + ">.")
        connections.disconnect("default")

    def has_partition(self, partition_name: str) -> bool:
        connections.connect("default")
        result = Collection(self.__collection_name).has_partition(partition_name)
        connections.disconnect("default")
        return result

    def insert(self, data: list, partition_name: str = "_default"):
        connections.connect("default")
        Collection(self.__collection_name).insert(data, partition_name)
        connections.disconnect("default")

    def do_bulk_insert(self, files: list[str], partition_name: str = "_default"):
        collection_name = self.__collection_name
        connections.connect("default")
        utility.do_bulk_insert(collection_name, files, partition_name)
        utility.wait_for_index_building_complete(collection_name)
        connections.disconnect("default")

    def drop_partition(self, partition_name: str = "_default"):
        connections.connect("default")
        Collection(self.__collection_name).drop_partition(partition_name)
        connections.disconnect("default")
        
    def load(self):
        collection_name = self.__collection_name
        connections.connect("default")
        collection = Collection(collection_name)
        collection.load()
        return collection
        
        
    def search(self, collection, data: list[float], anns_field: str, param: dict, limit: int, expr: str | None = None, partition_names: list[str] | None = None, output_fields: list[str] | None = None):
        results = collection.search(data, anns_field, param, limit, expr, partition_names, output_fields)
        # collection.release()
        # connections.disconnect("default")
        return results