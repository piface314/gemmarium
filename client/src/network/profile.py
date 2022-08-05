from nacl.public import PublicKey, SealedBox, Box
from network.endpoint import Endpoint
from nacl.encoding import Base64Encoder
from exceptions import InvalidUsernameError, UnknownError, UsernameTakenError, AuthError
import requests


class ProfileEndpoint(Endpoint):

    def __init__(self, vault_addr, vault_key: PublicKey):
        self.vault_addr = f'http://{vault_addr[0]}:{vault_addr[1]}'
        self.vault_key = vault_key

    def signup(self, username: str):
        res = requests.post(self.vault_addr+"/signup", json=dict(
            username=username, key=self.public_key.encode(Base64Encoder).decode()))
        if res.status_code != 200:
            error = res.json()['error']
            if error == 'InvalidUsername':
                raise InvalidUsernameError()
            if error == 'UsernameTaken':
                raise UsernameTakenError()
            raise UnknownError()
        return res.json()['id']

    def auth(self):
        res = requests.get(self.vault_addr+'/auth', params=dict(id=self.uid))
        if res.status_code != 200:
            raise AuthError()
        secret = res.json()['secret']
        secret = SealedBox(self.private_key).decrypt(secret, Base64Encoder)
        secret = Box(self.private_key, self.vault_key).encrypt(secret, encoder=Base64Encoder).decode()
        res2 = requests.post(self.vault_addr+'/auth', params=dict(id=self.uid), json=dict(secret=secret))
        if res2.status_code != 200:
            raise AuthError()
        return res2.json()['token']