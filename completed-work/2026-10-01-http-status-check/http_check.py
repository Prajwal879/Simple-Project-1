import sys
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
