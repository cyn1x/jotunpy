import os.path
import sqlite3

from core.config import CONFIG

con = sqlite3.connect(
    os.path.join(CONFIG['DATABASE']['FILEPATH'], CONFIG['DATABASE']['FILENAME']),
    check_same_thread=False
)

CREATE_TABLE = """CREATE TABLE blog(
              guid TEXT,
              title TEXT,
              description TEXT,
              author TEXT,
              published TEXT,
              link TEXT)"""


def create_table(name):
    c = con.cursor()
    if not table_exists(name):
        c.execute(CREATE_TABLE)
        con.commit()

    c.close()


def insert_blog_entry(meta):
    c = con.cursor()
    if item_exists(meta['link']):
        return

    c.execute(f"INSERT INTO blog VALUES ('"
              f"{meta['link']}',"
              f"'{meta['title']}',"
              f"'{meta['description']}',"
              f"'{meta['author']}',"
              f"'{meta['published']}',"
              f"'{meta['link']}')")
    con.commit()
    c.close()


def get_blog_entry(guid, *keys):
    c = con.cursor()
    query = c.execute("SELECT {} FROM blog WHERE guid=?;".format(', '.join(keys)), (guid,))
    rows = query.fetchone()
    c.close()

    return rows


def table_exists(table_name):
    c = con.cursor()
    query = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    exists = query.fetchone() is not None
    c.close()

    return exists


def item_exists(item):
    c = con.cursor()
    query = c.execute("SELECT * FROM blog WHERE guid=?", (item,))
    rows = query.fetchall()
    c.close()

    return rows != []
