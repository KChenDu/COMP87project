from utility import create_milvus_collection, milvus_collection_exists, drop_milvus_collection, create_sqlite_db, sqlite_db_exists, drop_sqlite_db


if __name__ == '__main__':
    if not milvus_collection_exists():
        create_milvus_collection()
    if not sqlite_db_exists():
        create_sqlite_db()
    if milvus_collection_exists():
        drop_milvus_collection()
    if sqlite_db_exists():
        drop_sqlite_db()
