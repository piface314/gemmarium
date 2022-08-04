from auth_ctrl import AuthCtrl
from nacl.public import PublicKey
import base64


class AuthEndpoint:

    def __init__(self, ctrl: AuthCtrl):
        self.ctrl = ctrl

    def signup(self):
        print(f"{context.peer()}: signup({str(request).strip()})")
        username = request.username
        pkey = request.key
        if not self.ctrl.is_username_valid(username):
            return dict(error="InvalidUsername")
        u = self.ctrl.add_user(username, pkey)
        if u is None:
            return dict(error="UsernameTaken")
        return dict(id=u.id)
        
    def auth(self, request_iterator, context):
        req = next(request_iterator)
        print(f'{context.peer()}: auth({str(req).strip()})')
        u = self.ctrl.get_user(req.id)
        if not u:
            yield dict(error="UserNotFound")
            return
        pkey = PublicKey(u.public_key)
        ref, secret = self.ctrl.get_secret(pkey)
        print(f"{context.peer()}: sending secret...")
        yield dict(secret=secret)
        req = next(request_iterator)
        if not self.ctrl.chk_secret(ref, req.secret, pkey):
            yield dict(error="AuthError")
            return
        print(f"{context.peer()}: sending token...")
        token = self.ctrl.get_token(u)
        yield dict(token=base64.b64encode(token).decode())


        
    