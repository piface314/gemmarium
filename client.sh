#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  vault_ip=$1
  vault_port=$2
  forge_ip=$3
  forge_port=$4
  search_ip=$5
  search_port=$6
  db_fp=$7
else
  vault_ip="127.0.0.1"
  vault_port="7513"
  forge_ip="127.0.0.1"
  forge_port="7514"
  search_ip=""
  search_port="7515"
  db_fp="client.db"
fi


cd client
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi
python3 src/main.py "$vault_ip" "$vault_port" "$forge_ip" "$forge_port" \
    "$search_ip" "$search_port" "$db_fp"