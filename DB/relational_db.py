import sqlite3

from pathlib import Path
from sqlite3 import Error


class SQLiteDB:
    def __init__(self, path: str = "test"):
        db_file = Path("sqlite/" + path + ".db")
        if not db_file.is_file():
            raise Exception("Database " + path + " does not exist.")
        self.__db_file = db_file

    def switch_to_db(self, name: str):
        db_file = Path("sqlite/" + name + ".db")
        if not db_file.is_file():
            raise Exception("Database " + name + " does not exist.")
        self.__db_file = db_file

    def create_table(self, name: str, fields: str):
        try:
            conn = sqlite3.connect(self.__db_file)
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS " + name + " (" + fields + ");")
            conn.close()
        except Error as e:
            print(e)

    def insert(self, table: str, values: list):
        for i, value in enumerate(values):
            if isinstance(value, str):
                values[i] = "'" + value.replace("'", "''") + "'"
            else:
                values[i] = str(value)
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + table + " VALUES(" + ', '.join(values) + ")")
        conn.commit()
        conn.close()

    def select(self, fields: list[str], table: str, condition: str | None = None):
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        if condition is None:
            cur.execute("SELECT " + ', '.join(fields) + " FROM " + table)
        else:
            cur.execute("SELECT " + ', '.join(fields) + " FROM " + table + " WHERE " + condition)
        rows = cur.fetchall()
        conn.close()
        return rows
