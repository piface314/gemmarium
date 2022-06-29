from forge_ctrl import ForgeCtrl
from nacl.encoding import Base64Encoder
from nacl.public import PublicKey
from server import Server, AuthError
import random
import socket


class ForgeEndpoint(Server):

    def __init__(self, port, private_key, public_key, vault_addr, vault_pkey: PublicKey, ctrl: ForgeCtrl):
        super().__init__(private_key, public_key)
        self.addr = ("", port)
        self.ctrl = ctrl
        self.vault_addr = vault_addr
        self.vault_pkey = vault_pkey

    def connect_vault(self, port):
        self.vault_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vault_socket.bind((self.addr[0], port))
        self.vault_socket.connect(self.vault_addr)

    def close(self):
        print("Closing socket with Vault")
        self.vault_socket.close()

    def auth(self, conn, addr, id: str):
        print(f"Thread@{addr}: authenticating...")
        vault_s = self.vault_socket
        msg = self.enc_msg(self.vault_pkey, "auth", id=id)
        self.send_size(vault_s, self.vault_pkey, msg)
        vault_s.sendall(msg)
        payload = vault_s.recv(1024)
        op, args = self.dec_msg(self.vault_pkey, payload)
        if op == 'error':
            raise AuthError()
        name, key = args['name'], args['key']

        print(f"Thread@{addr}: found {name} with key {key}...")
        pkey = PublicKey(key, Base64Encoder)
        secret = random.randint(0, 1<<32)
        print(f"Thread@{addr}: my secret is {secret}...")
        self.send(conn, pkey, "auth", secret=secret)
        payload = conn.recv(1024)
        op, args = self.dec_msg(pkey, payload)
        print(f"Thread@{addr}: their secret is {args['secret']}...")
        if op != 'auth' or args['secret'] != secret:
            raise AuthError()
        
        return name, pkey

    def handle_request(self, conn, addr, _, id: str, **args):
        username, pkey = self.auth(conn, addr, id)
        print(f"Thread@{addr}: checking quota...")
        ok, wait = self.ctrl.check_quota(id)
        if not ok:
            self.send(conn, pkey, "error", code="QuotaExceeded", wait=wait)
            return
        print(f"Thread@{addr}: choosing gem...")
        gem = self.ctrl.choose_gem(username)
        print(f"Thread@{addr}: sending gem...")
        self.send(conn, pkey, "gem", gem=gem)
        self.ctrl.set_quota(id)
    
    def handle_fusion(self, conn, addr, _, **args):
        pass
