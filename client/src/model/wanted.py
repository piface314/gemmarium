from model import Model
import threading


class Wanted(Model):

    __lock = threading.Lock()

    @classmethod
    def load(cls):
        db = cls.connect()
        return Wanted({gem for gem, in db.execute('SELECT * FROM wanted')})

    def __init__(self, gems: set[str]):
        self.gems = gems

    def add(self, gem: str):
        self.gems.add(gem)
        db = self.connect()
        with self.__lock:
            db.execute('REPLACE INTO wanted VALUES (?)', (gem,))
            db.commit()
        db.close()

    def remove(self, gem: str):
        self.gems.remove(gem)
        db = self.connect()
        with self.__lock:
            db.execute('DELETE FROM wanted WHERE gem=?', (gem,))
            db.commit()
        db.close()
