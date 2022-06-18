from auth_ctrl import AuthCtrl
from database import Database
from sys import argv

if __name__ == '__main__':
    db = Database()
    auth_ctrl = AuthCtrl(db, argv[1], int(argv[2]))
    auth_ctrl.run()
