from database import Database
from forge_ctrl import ForgeCtrl
from forge_endpoint import ForgeEndpoint
from nacl.public import PrivateKey, PublicKey
from nacl.signing import SigningKey, VerifyKey
from sys import argv
import keys


if __name__ == '__main__':
    vault_client_port = int(argv[4])
    db = Database()
    ctrl = ForgeCtrl(
        gem_time=int(argv[1]),
        db=db,
        sign_key=SigningKey(keys.forge_sign_key),
        verify_key=VerifyKey(keys.forge_vkey)
    )
    endp = ForgeEndpoint(
        addr=(argv[2], int(argv[3])),
        private_key=PrivateKey(keys.forge_skey),
        public_key=PublicKey(keys.forge_pkey),
        vault_addr=(argv[5], int(argv[6])),
        vault_pkey=PublicKey(keys.vault_pkey),
        ctrl=ctrl
    )
    endp.connect_vault(vault_client_port)
    endp.run()

    
