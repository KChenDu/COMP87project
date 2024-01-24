from pymilvus import FieldSchema, DataType, CollectionSchema


SCHEMA = CollectionSchema([FieldSchema(name="id", dtype=DataType.INT64, description="", is_primary=True),
                           FieldSchema(name="word_vector", dtype=DataType.FLOAT_VECTOR, dim=2)], "")

FIELD2INDEX_PARAMS = {
    "word_vector": {"metric_type": "L2", "index_type": "GPU_IVF_FLAT", "params": {"nlist": 1024}}
}
