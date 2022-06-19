with open("KEYS", "rb") as f:
    vault_skey = f.read(32)
    vault_pkey = f.read(32)
    forge_skey = f.read(32)
    forge_pkey = f.read(32)

with open("vault/src/keys.py", "w") as f:
    f.write(f'vault_skey = {vault_skey}\nvault_pkey = {vault_pkey}\nforge_pkey = {forge_pkey}\n')

with open("forge/src/keys.py", "w") as f:
    f.write(f'forge_skey = {forge_skey}\nforge_pkey = {forge_pkey}\nvault_pkey = {vault_pkey}\n')

with open("client/src/keys.py", "w") as f:
    f.write(f'forge_pkey = {forge_pkey}\nvault_pkey = {vault_pkey}\n')

