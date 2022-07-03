from auth_ctrl import AuthCtrl
from auth_endpoint import AuthEndpoint
from database import Database
from nacl.public import PrivateKey, PublicKey
from sys import argv
import keys

if __name__ == '__main__':
    vault_port = argv[1]
    db = Database()
    auth_ctrl = AuthCtrl(db)
    auth_endp = AuthEndpoint(
        port=int(vault_port),
        private_key=PrivateKey(keys.vault_skey),
        public_key=PublicKey(keys.vault_pkey),
        ctrl=auth_ctrl
    )
    auth_endp.listen()
