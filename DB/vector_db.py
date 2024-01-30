from pymilvus import connections, utility, Collection


class MilvusCollection:
    def __init__(self, name: str = "test"):
        connections.connect("default")
        if not utility.has_collection(name):
            raise Exception(f"Collection {name} does not exist.")
        connections.disconnect("default")
        self.__collection_name = name

    def switch_to_collection(self, name: str):
        connections.connect("default")
        if not utility.has_collection(name):
            raise Exception(f"Collection {name} does not exist.")
        connections.disconnect("default")
        self.__collection_name = name

    def create_partition(self, partition_name: str, description: str = ""):
        connections.connect("default")
        Collection(self.__collection_name).create_partition(partition_name, description)
        connections.disconnect("default")

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

    def search(self, data: list[float], anns_field: str, param: dict, limit: int, expr: str | None = None, partition_names: list[str] | None = None, output_fields: list[str] | None = None):
        collection_name = self.__collection_name
        connections.connect("default")
        collection = Collection(collection_name)
        collection.load()
        results = collection.search(data, anns_field, param, limit, expr, partition_names, output_fields)
        collection.release()
        connections.disconnect("default")
        return results
