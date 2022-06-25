import sqlite3


class Model:

    @classmethod
    def set_db_fp(cls, db_fp):
        cls.db_fp = db_fp
    
    @classmethod
    def create_db(cls, sql_fp):
        db = cls.connect()
        with open(sql_fp) as f:
            db.executescript(f.read())
        db.commit()
        db.close()

    @classmethod
    def connect(cls):
        return sqlite3.connect(cls.db_fp)