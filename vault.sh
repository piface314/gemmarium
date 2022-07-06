#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  vault_port=$1
else
  vault_port="7513"
fi

cd vault && \
  source .venv/bin/activate && \
  python3 src/main.py "$vault_port"
