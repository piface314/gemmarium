from auth_ctrl import AuthCtrl
from database import Database
from nacl.public import PrivateKey, PublicKey
from sys import argv
import keys

if __name__ == '__main__':
    db = Database()
    addr = (argv[1], int(argv[2]))
    forge_addr = (argv[3], int(argv[4]))
    auth_ctrl = AuthCtrl(
        addr=addr,
        private_key=PrivateKey(keys.vault_skey),
        public_key=PublicKey(keys.vault_pkey),
        db=db
    )
    auth_ctrl.trust_key(forge_addr, PublicKey(keys.forge_pkey))
    auth_ctrl.learn_host(forge_addr)
    auth_ctrl.run()
