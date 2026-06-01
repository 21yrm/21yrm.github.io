import html
import json
import os
import re
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SCHOLAR_URL = "https://scholar.google.com/citations?user={scholar_id}&hl=en"


def fetch_profile_html(scholar_id: str) -> str:
    request = Request(
        SCHOLAR_URL.format(scholar_id=scholar_id),
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_text(pattern: str, page: str) -> str | None:
    match = re.search(pattern, page, flags=re.DOTALL)
    if not match:
        return None
    value = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(value).strip()


def parse_profile(page: str, scholar_id: str) -> dict:
    name = extract_text(r'<div id="gsc_prf_in"[^>]*>(.*?)</div>', page)
    citation_cells = re.findall(r'<td class="gsc_rsb_std">([\d,]+)</td>', page)

    if not name or not citation_cells:
        page_title = extract_text(r"<title[^>]*>(.*?)</title>", page) or "unknown"
        snippet = re.sub(r"\s+", " ", page[:500]).strip()
        raise RuntimeError(
            "Google Scholar did not return a normal profile page. "
            f"title={page_title!r}, snippet={snippet!r}"
        )

    citedby = int(citation_cells[0].replace(",", ""))

    return {
        "scholar_id": scholar_id,
        "name": name,
        "citedby": citedby,
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": SCHOLAR_URL.format(scholar_id=scholar_id),
    }


def write_results(author: dict) -> None:
    os.makedirs("results", exist_ok=True)
    with open("results/gs_data.json", "w") as outfile:
        json.dump(author, outfile, ensure_ascii=False)

    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author['citedby']}",
    }
    with open("results/gs_data_shieldsio.json", "w") as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)


def main() -> None:
    scholar_id = os.environ["GOOGLE_SCHOLAR_ID"]
    print(f"Fetching Google Scholar stats for {scholar_id}", flush=True)

    try:
        page = fetch_profile_html(scholar_id)
        author = parse_profile(page, scholar_id)
    except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
        raise SystemExit(f"Failed to fetch Google Scholar stats: {error}") from error

    print(json.dumps(author, indent=2), flush=True)
    write_results(author)


if __name__ == "__main__":
    main()
