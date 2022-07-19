with open("KEYS", "rb") as f:
    vault_skey = f.read(32)
    vault_pkey = f.read(32)
    vault_sign_key = f.read(32)
    vault_vkey = f.read(32)
    forge_sign_key = f.read(32)
    forge_vkey = f.read(32)

with open("vault/src/keys.py", "w") as f:
    f.write(f'vault_skey = {vault_skey}\n')
    f.write(f'vault_pkey = {vault_pkey}\n')
    f.write(f'vault_sign_key = {vault_sign_key}\n')
    f.write(f'vault_vkey = {vault_vkey}\n')

with open("forge/src/keys.py", "w") as f:
    f.write(f'vault_vkey = {vault_vkey}\n')
    f.write(f'vault_pkey = {vault_pkey}\n')
    f.write(f'forge_sign_key = {forge_sign_key}\n')
    f.write(f'forge_vkey = {forge_vkey}\n')

with open("client/src/keys.py", "w") as f:
    f.write(f'vault_pkey = {vault_pkey}\n')
    f.write(f'forge_vkey = {forge_vkey}\n')

