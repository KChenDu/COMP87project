import argparse

from utility import sqlite_db_exists, drop_sqlite_db, create_sqlite_db, milvus_collection_exists, create_milvus_collection
from pathlib import Path
from loguru import logger
from setting import TABEL2FIELD
from relational_db import SQLiteDB
from json import load
from vector_db import MilvusCollection
from towhee import AutoConfig, AutoPipes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('collection')
    parser.add_argument('partition')
    parser.add_argument('data_path')
    args = parser.parse_args()

    data_path = Path(args.data_path)
    if not data_path.is_file():
        raise Exception(f"Dataset {data_path} does not exist.")

    collection_name = args.collection
    partition = args.partition

    keyword2context = {}

    # Create a relational db to store context and its id
    db = collection_name + '_' + partition
    if sqlite_db_exists(db):
        drop_sqlite_db(db)
    create_sqlite_db(db)
    db = SQLiteDB(db)
    for table, fields in TABEL2FIELD.items():
        db.create_table(table, fields)

    logger.debug(f"Creating keyword-to-contexts mapping for{data_path}.")

    # Read context-to-keywords json file and make keyword-to-contexts mapping
    with open(data_path, 'r') as f:
        data = load(f)

    for i, datum in enumerate(data):
        db.insert('context', [i, datum['context']])
        for keyword in datum['keywords']:
            if keyword in keyword2context:
                keyword2context[keyword].append(i)
            else:
                keyword2context[keyword] = [i]

    logger.debug("Keyword-to-contexts mapping created.")

    # Embed all keywords and insert into vector DB
    if not milvus_collection_exists(collection_name):
        create_milvus_collection(collection_name)
    collection = MilvusCollection()
    if not collection.has_partition(partition):
        collection.create_partition(partition)

    logger.debug("Populating partition <" + partition + '> in collection <' + collection_name + '>.')

    config = AutoConfig.load_config('sentence_embedding')
    config.model = 'average_word_embeddings_glove.6B.300d'
    sentence_embedding = AutoPipes.pipeline('sentence_embedding', config=config)

    keywords = list(keyword2context.keys())
    collection.insert([keywords,
                       [embedding.get()[0] for embedding in sentence_embedding.batch(keywords)],
                       list(keyword2context.values())], partition)

    logger.debug("Partition <" + partition + '> in collection <' + collection_name + '> populated.')
