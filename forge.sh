#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  forge_port=$1
  vault_ip=$2
  vault_port=$3
  gem_time=$5
else
  forge_port="7514"
  vault_ip="127.0.0.1"
  vault_port="7513"
  gem_time=10
fi

cd forge && \
  source .venv/bin/activate && \
  python3 src/main.py "$forge_port" "$vault_ip" "$vault_port" "$gem_time"
