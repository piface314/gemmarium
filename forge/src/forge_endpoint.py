from nacl.encoding import Base64Encoder
from server import Server
import socket



class ForgeEndpoint(Server):

    def __init__(self, addr, private_key, public_key, vault_addr, vault_pkey, ctrl):
        super().__init__(private_key, public_key)
        self.addr = addr
        self.ctrl = ctrl
        self.vault_addr = vault_addr
        self.trust_key(vault_addr, vault_pkey)

    def connect_vault(self, port):
        self.vault_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vault_socket.bind((self.addr[0], port))
        self.vault_socket.connect(self.vault_addr)

    def close(self):
        print("Closing socket with Vault")
        self.vault_socket.close()

    def handle_request(self, conn, addr, username, **args):
        print(f"Thread@{addr}: authenticating...")
        if not self.auth(addr, username):
            print(f"Thread@{addr}: auth error")
            conn.sendall(self.enc_msg(addr, "error", **args))
            return
        print(f"Thread@{addr}: checking quota...")
        ok, wait = self.ctrl.check_quota(username)
        if not ok:
            conn.sendall(self.enc_msg(addr, "error", code="QuotaExceeded", wait=wait))
            return
        print(f"Thread@{addr}: choosing gem...")
        gem = self.ctrl.choose_gem(username)
        print(f"Thread@{addr}: sending gem...")
        conn.sendall(self.enc_msg(addr, "gem", gem=gem))
        self.ctrl.set_quota(username)
    
    def handle_fusion(self, conn, addr, username, gems, **args):
        pass

    def auth(self, addr, username):
        msg = self.enc_msg(self.vault_addr, "key", username=username)
        self.vault_socket.sendall(msg)
        payload = self.vault_socket.recv(1024)
        op, args = self.dec_msg(self.vault_addr, payload)
        if op == 'error':
            return False
        self.trust_key(addr, args['key'], Base64Encoder)
        return True
