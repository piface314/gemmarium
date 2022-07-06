#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  search_port=$1
  vault_ip=$2
  vault_port=$3
  forge_ip=$4
  forge_port=$5
  db_fp=$6
  offset=$7
else
  search_port="7515"
  vault_ip="127.0.0.1"
  vault_port="7513"
  forge_ip="127.0.0.1"
  forge_port="7514"
  db_fp="client.db"
  offset="5"
fi


cd client && \
  source .venv/bin/activate && \
  python3 src/main.py "$search_port" "$vault_ip" "$vault_port" "$forge_ip" "$forge_port" "$db_fp" "$offset"