
KEYS=client/src/keys.py forge/src/keys.py vault/src/keys.py
SERVER_TEMPLATE=forge/src/server.py vault/src/server.py

all: $(KEYS) $(SERVER_TEMPLATE) client forge vault
	echo "OK"

client/src/keys.py: set_keys.py KEYS
	echo "Setting keys..."
	python set_keys.py

forge/src/keys.py: set_keys.py KEYS
	python set_keys.py

vault/src/keys.py: set_keys.py KEYS
	python set_keys.py

forge/src/server.py: server.py
	echo "Copying server template for Forge..."
	cp server.py forge/src/server.py

vault/src/server.py: server.py
	echo "Copying server template for Vault..."
	cp server.py vault/src/server.py

client:
	if [[ ! -d "client/.venv" ]]; then
		cd client
		python -m virtualenv .venv
		source .venv/bin/activate
		pip install -r requirements.txt
	fi

forge:
	if [[ ! -d "forge/.venv" ]]; then
		cd forge
		python -m virtualenv .venv
		source .venv/bin/activate
		pip install -r requirements.txt
	fi

vault:
	if [[ ! -d "vault/.venv" ]]; then
		cd vault
		python -m virtualenv .venv
		source .venv/bin/activate
		pip install -r requirements.txt
	fi

	