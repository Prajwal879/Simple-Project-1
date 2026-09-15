import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
try:
    with socket.create_connection((host, port), timeout=5):
        print(f"OPEN: {host}:{port}")
except OSError as error:
    print(f"CLOSED: {host}:{port} ({error})")
    raise SystemExit(1)
