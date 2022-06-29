from auth_ctrl import AuthCtrl
from nacl.public import PublicKey
from server import Server

class AuthEndpoint(Server):

    def __init__(self, port, private_key, public_key, ctrl: AuthCtrl):
        super().__init__(private_key, public_key)
        self.addr = ("", port)
        self.ctrl = ctrl

    def handle_signup(self, conn, addr, pkey: PublicKey, username: str, **args):
        print(f"Thread@{addr}: signing up...")
        if not self.ctrl.is_username_valid(username):
            print(f"Thread@{addr}: invalid name")
            self.send(conn, pkey, "error", code="InvalidUsername")
            return
        u = self.ctrl.add_user(username, pkey.encode())
        if u is None:
            print(f"Thread@{addr}: username taken")
            self.send(conn, pkey, "error", code="UsernameTaken")
            return
        print(f"Thread@{addr}: signed up")
        conn.sendall(self.enc_msg(pkey, "ack", id=u.id))
        self.send(conn, pkey, "ack", id=u.id)
          
    def handle_auth(self, conn, addr, pkey: PublicKey, id: str, **args):
        print(f"Thread@{addr}: finding user...")
        u = self.ctrl.get_user(id)
        if not u:
            print(f"Thread@{addr}: user not found")
            self.send(conn, pkey, "error", code="UserNotFound")
        print(f"Thread@{addr}: found user {u}")
        self.send(conn, pkey, "user", name=u.username, key=u.public_key)
