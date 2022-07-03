#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  vault_port=$1
else
  vault_port="7513"
fi

cd vault
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi
python3 src/main.py "$vault_port"
