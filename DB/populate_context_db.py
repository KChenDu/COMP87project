from argparse import ArgumentParser
from json import load
from utility import sqlite_db_exists, create_sqlite_db
from relational_db import SQLiteDB
from setting import TABEL2FIELD
from loguru import logger


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('language', choices=['en'])
    parser.add_argument('data_path')
    args = parser.parse_args()

    # Read context-to-keywords json file and make keyword-to-contexts mapping
    with open(args.data_path, 'r') as f:
        data = load(f)

    # Connect to the database, if it does not exist, create it
    if not sqlite_db_exists('context'):
        create_sqlite_db('context')
    language = args.language
    db = SQLiteDB('context')
    db.create_table(language, TABEL2FIELD['context'])

    logger.debug("Populating table <" + language + "> in database <context>")

    for datum in data:
        db.insert(language, [datum['id'], datum['context']])

    logger.debug("Populated table <" + language + "> in database <context>")
