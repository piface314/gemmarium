from nacl.public import PrivateKey, PublicKey
from exceptions import UsernameError


class ProfileEndpoint:

    def __init__(self, vault_key: PublicKey):
        self.__vault_key = vault_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey

    def signup(self, username: str, key: PublicKey):
        pass