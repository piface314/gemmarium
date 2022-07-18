#!/usr/bin/env bash
if [[ -n "$1" ]]; then
  forge_port=$1
  gem_time=$5
else
  forge_port="7514"
  gem_time=10
fi

cd forge && \
  source .venv/bin/activate && \
  python3 src/main.py "$forge_port" "$gem_time"
