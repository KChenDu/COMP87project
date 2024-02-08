from argparse import ArgumentParser
from utility import drop_milvus_collection, drop_sqlite_db


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('db_type', choices=['vector', 'relational'])
    parser.add_argument('db_name')
    args = parser.parse_args()

    db_type = args.db_type

    if db_type == 'vector':
        drop_milvus_collection(args.db_name)
    elif db_type == 'relational':
        drop_sqlite_db(args.db_name)
