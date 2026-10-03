import collections
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
