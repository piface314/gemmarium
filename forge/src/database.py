from collections import namedtuple
from datetime import datetime
import sqlite3
import threading

Quota = namedtuple('Quota', ['username', 'last_request_at'])


class Database:

    def __init__(self):
        self.__lock = threading.Lock()
        db = self.__connect()
        with open('res/create.sql') as f:
            sql = f.read()
            db.execute(sql)
            db.commit()

    def __connect(self):
        return sqlite3.connect('forge.db')

    def set_quota(self, username, last_request_at):
        db = self.__connect()
        with self.__lock:
            db.execute('INSERT OR REPLACE INTO quota VALUES (?, ?)',
                       (username, last_request_at))
            db.commit()

    def get_quota(self, username):
        db = self.__connect()
        c = db.execute('SELECT * FROM quota WHERE username = ?', (username,))
        q = c.fetchone()
        return None if q is None else Quota(q[0], datetime.fromisoformat(q[1]))
