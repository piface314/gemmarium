import base64
import json
import socket
import threading

def message(op, **args):
    return json.dumps([op, args]).encode('utf-8')

class AuthCtrl:

    def __init__(self, db, host, port=7513):
        self.db = db
        self.host = host
        self.port = port
        self.handlers = {
            "signup": self.handle_signup,
            "key": self.handle_key
        }

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                print("Listening...")
                conn, addr = s.accept()
                worker = threading.Thread(target=self.handle, args=(conn, addr))
                worker.start()
    
    def handle(self, conn, addr):
        with conn:
            print(f"Thread@{addr}: connected")
            try:
                request = conn.recv(1024)
                op, args = json.loads(request)
                self.handlers[op](conn, addr, **args)
            except KeyError:
                conn.sendall(message("error", code="UnknownOperation"))
            except TypeError:
                conn.sendall(message("error", code="UnknownArgument"))
            except Exception as e:
                print(e)
                conn.sendall(message("error", code="UnknownError"))

    def handle_signup(self, conn, addr, username, key):
        if self.db.add_user(username, base64.b64decode(key)):
            print(f"Thread@{addr}: signed up")
            conn.sendall(message("ack"))
        else:
            conn.sendall(message("error", code="UsernameTaken"))
        
    def handle_key(self, conn, addr, username):
        u = self.db.get_user(username)
        if u:
            print(f"Thread@{addr}: found key {u.public_key}")
            conn.sendall(message("key", key=base64.b64encode(u.public_key).decode()))
        else:
            conn.sendall(message("error", code="UserNotFound"))