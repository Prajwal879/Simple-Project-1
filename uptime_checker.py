#!/usr/bin/env python3
"""Check whether one or more websites are reachable."""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CheckResult:
    url: str
    is_up: bool
    status: int | None
    elapsed_ms: int
    message: str


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("website URL cannot be empty")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url


def check_website(url: str, timeout: float = 5.0) -> CheckResult:
    url = normalize_url(url)
    request = Request(url, headers={"User-Agent": "Simple-Uptime-Checker/1.0"})
    started = time.perf_counter()

    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            is_up = 200 <= status < 400
            message = "reachable" if is_up else f"returned HTTP {status}"
    except HTTPError as error:
        status = error.code
        is_up = False
        message = f"returned HTTP {status}"
    except (URLError, TimeoutError, OSError) as error:
        status = None
        is_up = False
        message = str(getattr(error, "reason", error))

    elapsed_ms = round((time.perf_counter() - started) * 1000)
    return CheckResult(url, is_up, status, elapsed_ms, message)


def read_sites(path: str) -> list[str]:
    with open(path, encoding="utf-8") as stream:
        return [line.strip() for line in stream if line.strip() and not line.lstrip().startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether websites are up or down")
    parser.add_argument("urls", nargs="*", help="website URLs to check")
    parser.add_argument("--file", default="sites.txt", help="text file containing one URL per line")
    parser.add_argument("--timeout", type=float, default=5.0, help="timeout in seconds (default: 5)")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        urls = args.urls or read_sites(args.file)
    except OSError as error:
        parser.error(str(error))

    if not urls:
        parser.error("provide a URL or add one to the sites file")

    failed = False
    for url in urls:
        result = check_website(url, args.timeout)
        symbol = "[UP]  " if result.is_up else "[DOWN]"
        print(f"{symbol}  {result.url}  {result.elapsed_ms} ms  ({result.message})")
        failed = failed or not result.is_up

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
