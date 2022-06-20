from auth_ctrl import AuthCtrl
from database import Database
from nacl.encoding import RawEncoder
from sys import argv
import keys

if __name__ == '__main__':
    db = Database()
    addr = (argv[1], int(argv[2]))
    forge_addr = (argv[3], int(argv[4]))
    auth_ctrl = AuthCtrl(
        addr=addr,
        private_key=keys.vault_skey,
        public_key=keys.vault_pkey,
        db=db
    )
    auth_ctrl.trust_key(forge_addr, keys.forge_pkey, RawEncoder)
    auth_ctrl.learn_host(forge_addr)
    auth_ctrl.run()
