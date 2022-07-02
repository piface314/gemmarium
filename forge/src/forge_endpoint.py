from forge_ctrl import ForgeCtrl
from nacl.encoding import Base64Encoder
from nacl.public import PublicKey
from server import Server, AuthError
from time import time
import random
import socket
import traceback


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
        msg = self.enc_msg(pkey, "auth", secret=secret)
        conn.sendall(msg)
        print(f"Thread@{addr}: secret bytes {len(msg)} {msg}...")
        payload = conn.recv(1024)
        try:
            op, args = self.dec_msg(pkey, payload)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise AuthError()
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
    
    def handle_fusion(self, conn, addr, _, id: str, peerid: str, gems, **args):
        username, pkey = self.auth(conn, addr, id)
        print(f"Thread@{addr}: attempting fusion...")
        try:
            self.ctrl.update_fusion_request(id, peerid, id, username, gems)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.ctrl.remove_fusion_request(id, peerid)
            msg = self.enc_msg(pkey, 'error', code='InvalidGems')
            self.send_size(conn, pkey, msg)
            conn.sendall(msg)
            return
        t0 = time()
        ok = False
        print(f"Thread@{addr}: waiting for peer...")
        try:
            while time() - t0 <= 60:
                req = self.ctrl.get_fusion_request(id, peerid)
                if req.is_complete() and req.has_fusion_set():
                    print(f"Thread@{addr}: peer connected")
                    ok = True
                    break
        except:
            pass
        if not ok:
            print(f"Thread@{addr}: timeout")
            msg = self.enc_msg(pkey, 'error', code='Timeout')
            self.send_size(conn, pkey, msg)
            conn.sendall(msg)
            return
        req = self.ctrl.get_fusion_request(id, peerid)
        fused, others = req.fusion
        gems = [fused, *others[id]] if fused else others[id]
        msg = self.enc_msg(pkey, "gems", gems=gems)
        self.send_size(conn, pkey, msg)
        conn.sendall(msg)
        self.ctrl.remove_fusion_request(id, peerid)
        
        
