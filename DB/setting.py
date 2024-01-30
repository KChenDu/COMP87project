from pymilvus import FieldSchema, DataType, CollectionSchema


SCHEMA = CollectionSchema([FieldSchema("keyword", DataType.VARCHAR, is_primary=True, max_length=512),
                           FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=300),
                           FieldSchema("context_ids", DataType.ARRAY, element_type=DataType.INT64, max_length=32, max_capacity=1024)])

METRIC_TYPE = "COSINE"

# "index_type" must be set according to CPU/GPU version
FIELD2INDEX_PARAMS = {
    "embedding": {"metric_type": METRIC_TYPE, "index_type": "GPU_IVF_FLAT", "params": {"nlist": 128}},
}
