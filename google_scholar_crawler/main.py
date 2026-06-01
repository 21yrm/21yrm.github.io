import html
import json
import os
import re
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SCHOLAR_URL = "https://scholar.google.com/citations?user={scholar_id}&hl=en"
SERPAPI_URL = "https://serpapi.com/search.json"
DEFAULT_AUTHOR_NAME = "Runmao Yao"


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


def fetch_serpapi_profile(scholar_id: str, api_key: str) -> dict:
    params = urlencode(
        {
            "engine": "google_scholar_author",
            "author_id": scholar_id,
            "hl": "en",
            "api_key": api_key,
        }
    )
    request = Request(
        f"{SERPAPI_URL}?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": "21yrm.github.io citation updater",
        },
    )

    with urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_serpapi_profile(data: dict, scholar_id: str) -> dict:
    if data.get("error"):
        raise RuntimeError(data["error"])

    author = data.get("author") or {}
    cited_by = data.get("cited_by") or {}
    table = cited_by.get("table") or []
    citations = table[0].get("citations", {}) if table else {}
    citedby = citations.get("all")

    if not isinstance(citedby, int):
        raise RuntimeError("SerpAPI response did not include cited_by.table[0].citations.all")

    name = author.get("name") or DEFAULT_AUTHOR_NAME
    source = data.get("search_metadata", {}).get("google_scholar_author_url")
    return build_author(
        scholar_id,
        name,
        citedby,
        source or SCHOLAR_URL.format(scholar_id=scholar_id),
    )


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

    return build_author(scholar_id, name, citedby, SCHOLAR_URL.format(scholar_id=scholar_id))


def build_author(scholar_id: str, name: str, citedby: int, source: str) -> dict:
    return {
        "scholar_id": scholar_id,
        "name": name,
        "citedby": citedby,
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": source,
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

    citedby_override = os.environ.get("CITEDBY_OVERRIDE", "").strip()
    serpapi_api_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if citedby_override:
        try:
            citedby = int(citedby_override.replace(",", ""))
        except ValueError as error:
            raise SystemExit(f"Invalid CITEDBY_OVERRIDE value: {citedby_override}") from error
        author = build_author(scholar_id, DEFAULT_AUTHOR_NAME, citedby, "manual workflow input")
    elif serpapi_api_key:
        try:
            data = fetch_serpapi_profile(scholar_id, serpapi_api_key)
            author = parse_serpapi_profile(data, scholar_id)
        except (HTTPError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as error:
            raise SystemExit(f"Failed to fetch Google Scholar stats from SerpAPI: {error}") from error
    else:
        try:
            page = fetch_profile_html(scholar_id)
            author = parse_profile(page, scholar_id)
        except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
            raise SystemExit(f"Failed to fetch Google Scholar stats: {error}") from error

    print(json.dumps(author, indent=2), flush=True)
    write_results(author)


if __name__ == "__main__":
    main()
