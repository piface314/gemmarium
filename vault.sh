#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  vault_ip=$1
  vault_port=$2
  forge_ip=$3
  forge_port=$4
else
  vault_ip="127.0.0.1"
  vault_port="7513"
  forge_ip="127.0.0.1"
  forge_port="7512"
fi

cd vault \
  && source .venv/bin/activate \
  && python3 src/main.py "$vault_ip" "$vault_port" "$forge_ip" "$forge_port"