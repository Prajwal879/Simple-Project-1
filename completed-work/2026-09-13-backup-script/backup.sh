#!/bin/sh
set -eu
source_dir="${1:?Usage: backup.sh SOURCE BACKUP_DIR}"
backup_dir="${2:?Usage: backup.sh SOURCE BACKUP_DIR}"
mkdir -p "$backup_dir"
name=$(basename "$source_dir")
timestamp=$(date +%Y%m%d-%H%M%S)
archive="$backup_dir/${name}-${timestamp}.tar.gz"
tar -czf "$archive" -C "$(dirname "$source_dir")" "$name"
echo "Created $archive"
