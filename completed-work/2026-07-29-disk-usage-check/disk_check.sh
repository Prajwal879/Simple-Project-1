#!/bin/sh
set -eu
threshold="${THRESHOLD:-85}"
path="${1:-/}"
usage=$(df -P "$path" | awk 'NR==2 {gsub(/%/, "", $5); print $5}')
if [ "$usage" -ge "$threshold" ]; then
  echo "WARNING: $path is ${usage}% full"
  exit 1
fi
echo "OK: $path is ${usage}% full"
