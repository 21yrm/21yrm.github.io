#!/usr/bin/env python3
"""Fetch public FlagCounter total pageviews for the homepage footer."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import urllib.request
from pathlib import Path


DEFAULT_COUNTER_ID = "4jbg"
DEFAULT_OUTPUT = Path("assets/data/flagcounter.json")


def clean_text(document: str) -> str:
    document = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", document)
    document = re.sub(r"(?s)<[^>]+>", " ", document)
    return re.sub(r"\s+", " ", html.unescape(document)).strip()


def parse_total_views(document: str) -> int | None:
    text = clean_text(document)
    match = re.search(r"counter\s+has\s+been\s+viewed\s+([\d,]+)\s+times?", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1).replace(",", ""))

    return parse_history_table_views(document)


def parse_history_table_views(document: str) -> int | None:
    rows = re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", document)
    total = 0
    found_view_cells = False
    for row in rows:
        cells = re.findall(r"(?is)<td[^>]*>(.*?)</td>", row)
        if len(cells) < 3:
            continue
        date_cell = clean_text(cells[0])
        views_cell = clean_text(cells[2])
        if not date_cell or "Flag Counter Views" in views_cell:
            continue
        match = re.search(r"([\d,]+)", views_cell)
        if not match:
            continue
        found_view_cells = True
        total += int(match.group(1).replace(",", ""))
    return total if found_view_cells else None


def fetch_document(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "21yrm.github.io flagcounter updater"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def write_json(output: Path, total_views: int | None, stats_url: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "total_views": total_views,
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
    total_views = data.get("total_views")
    return total_views if isinstance(total_views, int) else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counter-id", default=os.environ.get("FLAGCOUNTER_ID", DEFAULT_COUNTER_ID))
    parser.add_argument("--url", default=os.environ.get("FLAGCOUNTER_STATS_URL", ""))
    parser.add_argument("--input-html", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    stats_url = args.url or f"https://www.flagcounter.com/more30/{args.counter_id}/"
    document = args.input_html.read_text(encoding="utf-8") if args.input_html else fetch_document(stats_url)
    total_views = parse_total_views(document)
    if total_views is None:
        total_views = read_existing_total(args.output)
    if total_views is None:
        total_views = 0
        print("Could not parse total FlagCounter views; publishing 0 fallback.")
    write_json(args.output, total_views, stats_url)
    print(f"Fetched FlagCounter total views: {total_views}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
