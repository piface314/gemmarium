#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  vault_port=$1
  forge_ip=$2
  forge_port=$3
else
  vault_port="7513"
  forge_ip="127.0.0.1"
  forge_port="7512"
fi

cd vault
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi
python3 src/main.py "$vault_port" "$forge_ip" "$forge_port"
