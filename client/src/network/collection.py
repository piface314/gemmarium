from nacl.public import PrivateKey, PublicKey
from nacl.signing import VerifyKey
from exceptions import QuotaError


class CollectionEndpoint:

    def __init__(self, forge_key: PublicKey, verify_key: VerifyKey):
        self.__forge_key = forge_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey
    
    def request_gem(self):
        pass
