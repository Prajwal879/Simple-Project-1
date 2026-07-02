#!/usr/bin/env python3
"""Build one small, useful DevOps tool and a readable report each day."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TASKS = [
    {
        "slug": "disk-usage-check",
        "title": "Disk Usage Check",
        "summary": "Added a shell utility that warns when a filesystem is nearly full.",
        "run": "THRESHOLD=80 sh disk_check.sh /",
        "files": {
            "disk_check.sh": '''#!/bin/sh
set -eu
threshold="${THRESHOLD:-85}"
path="${1:-/}"
usage=$(df -P "$path" | awk 'NR==2 {gsub(/%/, "", $5); print $5}')
if [ "$usage" -ge "$threshold" ]; then
  echo "WARNING: $path is ${usage}% full"
  exit 1
fi
echo "OK: $path is ${usage}% full"
''',
        },
    },
    {
        "slug": "http-status-check",
        "title": "HTTP Status Check",
        "summary": "Added a small Python command that checks an endpoint and returns a CI-friendly exit code.",
        "run": "python http_check.py https://example.com",
        "files": {
            "http_check.py": '''import sys
from urllib.error import URLError
from urllib.request import urlopen

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
try:
    with urlopen(url, timeout=5) as response:
        print(f"UP: {url} returned HTTP {response.status}")
        raise SystemExit(0 if response.status < 400 else 1)
except (URLError, TimeoutError) as error:
    print(f"DOWN: {url} ({error})")
    raise SystemExit(1)
''',
        },
    },
    {
        "slug": "docker-compose-health",
        "title": "Healthy Docker Compose Service",
        "summary": "Added a minimal Nginx service with a restart policy and container health check.",
        "run": "docker compose up -d && docker compose ps",
        "files": {
            "compose.yaml": '''services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 10s
      timeout: 3s
      retries: 3
''',
        },
    },
    {
        "slug": "log-error-counter",
        "title": "Log Error Counter",
        "summary": "Added a dependency-free utility that counts errors and warnings in a log file.",
        "run": "python count_logs.py example.log",
        "files": {
            "count_logs.py": '''import collections
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "example.log"
counts = collections.Counter()
with open(path, encoding="utf-8", errors="replace") as stream:
    for line in stream:
        upper = line.upper()
        level = next((item for item in ("ERROR", "WARNING", "INFO") if item in upper), "OTHER")
        counts[level] += 1
for level in ("ERROR", "WARNING", "INFO", "OTHER"):
    print(f"{level}: {counts[level]}")
''',
            "example.log": "INFO service started\nWARNING response is slow\nERROR connection failed\n",
        },
    },
    {
        "slug": "backup-script",
        "title": "Timestamped Backup Script",
        "summary": "Added a safe shell utility that creates a compressed, timestamped directory backup.",
        "run": "sh backup.sh ./my-folder ./backups",
        "files": {
            "backup.sh": '''#!/bin/sh
set -eu
source_dir="${1:?Usage: backup.sh SOURCE BACKUP_DIR}"
backup_dir="${2:?Usage: backup.sh SOURCE BACKUP_DIR}"
mkdir -p "$backup_dir"
name=$(basename "$source_dir")
timestamp=$(date +%Y%m%d-%H%M%S)
archive="$backup_dir/${name}-${timestamp}.tar.gz"
tar -czf "$archive" -C "$(dirname "$source_dir")" "$name"
echo "Created $archive"
''',
        },
    },
    {
        "slug": "kubernetes-health-probes",
        "title": "Kubernetes Health Probes",
        "summary": "Added a basic Deployment that demonstrates readiness and liveness checks.",
        "run": "kubectl apply -f deployment.yaml",
        "files": {
            "deployment.yaml": '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthy-web
spec:
  replicas: 1
  selector:
    matchLabels: {app: healthy-web}
  template:
    metadata:
      labels: {app: healthy-web}
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet: {path: /, port: 80}
          livenessProbe:
            httpGet: {path: /, port: 80}
''',
        },
    },
    {
        "slug": "service-port-check",
        "title": "Service Port Check",
        "summary": "Added a Python utility that verifies whether a TCP service accepts connections.",
        "run": "python port_check.py github.com 443",
        "files": {
            "port_check.py": '''import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
try:
    with socket.create_connection((host, port), timeout=5):
        print(f"OPEN: {host}:{port}")
except OSError as error:
    print(f"CLOSED: {host}:{port} ({error})")
    raise SystemExit(1)
''',
        },
    },
]


def task_for(day: date) -> dict:
    return TASKS[day.toordinal() % len(TASKS)]


def next_task(root: Path) -> dict:
    """Choose the first project type that has not been built yet."""
    completed_root = root / "completed-work"
    folder_names = [path.name for path in completed_root.iterdir() if path.is_dir()] if completed_root.exists() else []
    for task in TASKS:
        if not any(name.endswith(f"-{task['slug']}") for name in folder_names):
            return task
    return TASKS[len(folder_names) % len(TASKS)]


def build(day: date, root: Path) -> tuple[Path, dict]:
    task = next_task(root)
    destination = root / "completed-work" / f"{day.isoformat()}-{task['slug']}"
    destination.mkdir(parents=True, exist_ok=True)
    for relative_path, content in task["files"].items():
        output = destination / relative_path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    file_list = "\n".join(f"- `{name}`" for name in task["files"])
    readme = f"""# {task['title']}

**Completed:** {day.isoformat()}

{task['summary']}

## Run it

```bash
{task['run']}
```

## Files created

{file_list}

This small task was implemented automatically by the free Daily DevOps Builder.
"""
    (destination / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    return destination, task


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    output, task = build(args.date, args.output_root)
    print(f"TASK_DATE={args.date.isoformat()}")
    print(f"TASK_TITLE={task['title']}")
    print(f"TASK_SUMMARY={task['summary']}")
    print(f"TASK_PATH={output.relative_to(args.output_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
