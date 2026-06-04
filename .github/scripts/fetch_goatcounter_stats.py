#!/usr/bin/env python3
"""Fetch GoatCounter total pageviews for the homepage footer."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from typing import Any


DEFAULT_CODE = "yaorunmao"
DEFAULT_OUTPUT = Path("assets/data/goatcounter.json")
DEFAULT_START = "2026-06-01T00:00:00Z"
LEGACY_VIEWS_OFFSET = 2208


def extract_total_views(data: dict[str, Any]) -> int | None:
    total = data.get("total")
    return total if isinstance(total, int) else None


def merge_legacy_offset(goatcounter_views: int | None) -> int | None:
    return goatcounter_views + LEGACY_VIEWS_OFFSET if goatcounter_views is not None else None


def build_stats_url(api_base: str, start: str) -> str:
    end = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat()
    query = urllib.parse.urlencode({"start": start, "end": end})
    return f"{api_base.rstrip('/')}/stats/total?{query}"


def fetch_stats(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "21yrm.github.io goatcounter updater",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(f"GoatCounter API request failed: {error.code} {error.reason} for {url}")
        print(body[:1000])
        raise


def write_json(output: Path, goatcounter_views: int | None, stats_url: str) -> None:
    total_views = merge_legacy_offset(goatcounter_views)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "total_views": total_views,
        "goatcounter_views": goatcounter_views,
        "legacy_views_offset": LEGACY_VIEWS_OFFSET,
        "stats_url": stats_url,
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }, indent=2) + "\n", encoding="utf-8")


def read_existing_total(output: Path) -> int | None:
    if not output.exists():
        return None
    try:
        data = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    goatcounter_views = data.get("goatcounter_views")
    if isinstance(goatcounter_views, int):
        return goatcounter_views
    total_views = data.get("total_views")
    if isinstance(total_views, int):
        return max(total_views - LEGACY_VIEWS_OFFSET, 0)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code", default=os.environ.get("GOATCOUNTER_CODE", DEFAULT_CODE))
    parser.add_argument("--token", default=os.environ.get("GOATCOUNTER_TOKEN", ""))
    parser.add_argument("--api-base", default=os.environ.get("GOATCOUNTER_API_BASE", ""))
    parser.add_argument("--start", default=os.environ.get("GOATCOUNTER_START", DEFAULT_START))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    code = args.code or DEFAULT_CODE
    api_base = args.api_base or f"https://{code}.goatcounter.com/api/v0"
    stats_url = build_stats_url(api_base, args.start)

    goatcounter_views = read_existing_total(args.output)
    if args.token:
        goatcounter_views = extract_total_views(fetch_stats(stats_url, args.token))
    else:
        print("GOATCOUNTER_TOKEN is not set; publishing existing value.")

    write_json(args.output, goatcounter_views, stats_url)
    total_views = merge_legacy_offset(goatcounter_views)
    print(f"Fetched GoatCounter total views: {total_views}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
