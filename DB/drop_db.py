from argparse import ArgumentParser
from utility import drop_milvus_collection, drop_sqlite_db


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('db_type', choices=['vector', 'relational'])
    parser.add_argument('db_name')
    args = parser.parse_args()

    db_type = args.db_type

    if db_type == 'vector':
        db_name = args.db_name
        drop_milvus_collection(db_name)
    elif db_type == 'relational':
        db_name = args.db_name
        drop_sqlite_db(db_name)
