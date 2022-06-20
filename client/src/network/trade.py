from nacl.public import PrivateKey, PublicKey
from nacl.signing import VerifyKey
from model.trade import Trade


class TradeEndpoint:

    def __init__(self, verify_key: VerifyKey):
        self.__listeners = []
        self.__connections = {}
        self.__verify_key = verify_key

    def set_keys(self, skey: PrivateKey, pkey: PublicKey):
        self.__private_key = skey
        self.__public_key = pkey

    def listen(self):
        pass

    def update(self, trade: Trade):
        pass

    def accept(self, trade: Trade):
        pass

    def reject(self, trade: Trade):
        pass

    def fuse(self, trade: Trade):
        pass
