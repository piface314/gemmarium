from auth_ctrl import AuthCtrl
from auth_endpoint import AuthEndpoint
from database import Database
from nacl.public import PrivateKey
from nacl.signing import SigningKey
from sys import argv
import keys


if __name__ == '__main__':
    port = argv[1]
    db = Database()
    ctrl = AuthCtrl(db, SigningKey(keys.vault_sign_key), PrivateKey(keys.vault_skey))
    endp = AuthEndpoint(ctrl)
    print(f"Vault started!")
    endp.app.run(port=port, debug=True)


    
