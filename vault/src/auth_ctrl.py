from server import Server
import base64

class AuthCtrl(Server):

    def __init__(self, addr, private_key, public_key, db):
        super().__init__(private_key, public_key)
        self.db = db
        self.addr = addr

    def handle_signup(self, conn, addr, username, key, **args):
        print(f"Thread@{addr}: signing up...")
        if self.db.add_user(username, base64.b64decode(key)):
            print(f"Thread@{addr}: signed up")
            conn.sendall(self.send_msg(addr, "ack"))
        else:
            conn.sendall(self.send_msg(addr, "error", code="UsernameTaken"))
        
    def handle_key(self, conn, addr, username, **args):
        print(f"Thread@{addr}: finding key...")
        u = self.db.get_user(username)
        if u:
            key = base64.b64encode(u.public_key).decode()
            print(f"Thread@{addr}: found key {key}")
            conn.sendall(self.send_msg(addr, "key", key=key))
        else:
            print(f"Thread@{addr}: key not found")
            conn.sendall(self.send_msg(addr, "error", code="UserNotFound"))
