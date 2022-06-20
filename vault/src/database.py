from collections import namedtuple
import sqlite3
import threading


User = namedtuple('User', ['username', 'public_key'])


class Database:

    __user_query = 'SELECT * FROM user WHERE username = ?'

    def __init__(self):
        db = self.__connect()
        self.__lock = threading.Lock()
        with open('res/create.sql') as f:
            sql = f.read()
            db.executescript(sql)
            db.commit()
    
    def __connect(self):
        return sqlite3.connect('vault.db')

    def add_user(self, username, public_key):
        db = self.__connect()
        with self.__lock:
            if db.execute(self.__user_query, (username,)).fetchone() is not None:
                return False
            db.execute('INSERT INTO user VALUES (?, ?)',
                            (username, public_key))
            db.commit()
            db.close()
            return True

    def get_user(self, username):
        db = self.__connect()
        c = db.execute(self.__user_query, (username,))
        u = c.fetchone()
        db.close()
        return None if u is None else User(*u)
