from auth_ctrl import AuthCtrl
from nacl.public import PublicKey
from rmi.vault_pb2_grpc import AuthServicer
from rmi.vault_pb2 import SignupResponse, AuthResponse


class AuthEndpoint(AuthServicer):

    def __init__(self, port, ctrl: AuthCtrl):
        self.addr = ("", port)
        self.ctrl = ctrl

    def signup(self, request, context):
        print(f"signup({str(request).strip()})")
        username = request.username
        pkey = request.key
        if not self.ctrl.is_username_valid(username):
            return SignupResponse(error="InvalidUsername")
        u = self.ctrl.add_user(username, pkey)
        if u is None:
            return SignupResponse(error="UsernameTaken")
        return SignupResponse(id=u.id)
        
    def auth(self, request_iterator, context):
        print(context)
        req = next(request_iterator)
        print(f'auth({str(req).strip()})')
        u = self.ctrl.get_user(req.id)
        if not u:
            print(f'error: user not found')
            yield AuthResponse(error="UserNotFound")
            return
        pkey = PublicKey(u.public_key)
        ref, secret = self.ctrl.get_secret(pkey)
        print(f"sending secret...")
        yield AuthResponse(secret=secret)
        req = next(request_iterator)
        print(f'auth({str(req).strip()})')
        if not self.ctrl.chk_secret(ref, req.secret, pkey):
            print(f'error: auth error')
            yield AuthResponse(error="AuthError")
            return
        token = self.ctrl.get_token(u)
        yield AuthResponse(token=token)


        
    