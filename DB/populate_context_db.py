from argparse import ArgumentParser
from json import load
from utility import sqlite_db_exists, create_sqlite_db
from relational_db import SQLiteDB
from setting import TABEL2FIELD
from loguru import logger


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('db_name')
    parser.add_argument('language', choices=['en', 'zh'])
    parser.add_argument('data_path')
    args = parser.parse_args()

    # Read context-to-keywords json file and make keyword-to-contexts mapping
    with open(args.data_path, 'r') as f:
        data = load(f)

    # Connect to the database, if it does not exist, create it

    db_name = args.db_name

    if not sqlite_db_exists(db_name):
        create_sqlite_db(db_name)
    language = args.language
    db = SQLiteDB(db_name)
    db.create_table(language, TABEL2FIELD['context'])

    logger.debug("Populating table <" + language + "> in database <" + db_name + '>')

    for datum in data:
        db.insert(language, [datum['id'], datum['context']])

    logger.debug("Populated table <" + language + "> in database <" + db_name + '>')
