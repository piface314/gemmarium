#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  search_port=$1
  trade_port=$2
  vault_ip=$3
  vault_port=$4
  forge_ip=$5
  forge_port=$6
  db_fp=$7
  offset=$8
else
  search_port="7515"
  trade_port="7516"
  vault_ip="127.0.0.1"
  vault_port="7513"
  forge_ip="127.0.0.1"
  forge_port="7514"
  db_fp="client.db"
  offset="5"
fi


cd client
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi
python3 src/main.py "$search_port" "$trade_port" \
    "$vault_ip" "$vault_port" "$forge_ip" "$forge_port" "$db_fp" "$offset"