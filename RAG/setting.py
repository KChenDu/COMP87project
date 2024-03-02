from pymilvus import FieldSchema, DataType, CollectionSchema

DIMENSION = 1536
SCHEMA = CollectionSchema([
    FieldSchema(name='id', dtype=DataType.INT64,is_primary=True),
    FieldSchema(name='sub_id', dtype=DataType.INT64),
    FieldSchema(name='context_embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
])

METRIC_TYPE = "COSINE"

# "metric_type" must be set according to embedding algorithm
# "index_type" must be set according to CPU/GPU version
FIELD2INDEX_PARAMS = {
    "context_embedding": {
    'metric_type':"COSINE",
    'index_type':"IVF_FLAT",
    'params':{"nlist": 1024}
}
}

TABEL2FIELD = {
    "context": "id integer PRIMARY KEY, context text NOT NULL"
}
