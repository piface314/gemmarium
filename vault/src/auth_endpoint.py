from auth_ctrl import AuthCtrl
from nacl.public import PublicKey
from nacl.utils import random
from flask import Flask, request
import base64
import threading


class AuthEndpoint:

    def __init__(self, ctrl: AuthCtrl):
        self.ctrl = ctrl
        self.app = Flask(__name__)
        self.app.secret_key = random(32)
        self.app.route("/signup", methods=["POST"])(self.signup)
        self.app.route("/auth", methods=["GET", "POST"])(self.auth)
        self.session = {}
    
    def signup(self):
        body = request.get_json()
        username = body['username']
        pkey = base64.b64decode(body['key'])
        if not self.ctrl.is_username_valid(username):
            return dict(error="InvalidUsername"), 400
        u = self.ctrl.add_user(username, pkey)
        if u is None:
            return dict(error="UsernameTaken"), 400
        return dict(id=u.id)
    
    def auth(self):
        if request.method == 'GET':
            uid = request.args.get("id")
            u = self.ctrl.get_user(uid)
            if not u:
                return dict(error="UserNotFound"), 404
            pkey = PublicKey(u.public_key)
            ref, secret = self.ctrl.get_secret(pkey)
            self.session[uid] = (ref, pkey)
            threading.Timer(30, lambda: self.session.pop(uid,None)).start()
            return dict(secret=base64.b64encode(secret).decode())
        body = request.get_json()
        uid = request.args.get("id")
        if uid not in self.session:
            return dict(error="AuthError"), 401
        ref, pkey = self.session[uid]
        u = self.ctrl.get_user(uid)
        if not self.ctrl.chk_secret(ref, base64.b64decode(body['secret']), pkey):
            return dict(error="AuthError"), 401
        token = self.ctrl.get_token(u)
        return dict(token=base64.b64encode(token).decode())


        
    