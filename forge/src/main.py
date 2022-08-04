from database import Database
from forge_ctrl import ForgeCtrl
from forge_endpoint import ForgeEndpoint
from nacl.signing import SigningKey, VerifyKey
from sys import argv
import keys


if __name__ == '__main__':
    port, gem_time = argv[1:5]
    db = Database()
    ctrl = ForgeCtrl(
        db=db,
        gem_time=int(gem_time),
        sign_key=SigningKey(keys.forge_sign_key),
        verify_key=VerifyKey(keys.forge_vkey),
        vault_vkey=VerifyKey(keys.vault_vkey)
    )
    endp = ForgeEndpoint(ctrl)
    print(f"Forge started!")
    endp.app.run(port=port, debug=True)
