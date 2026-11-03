"""Bounded Browser Run acquisition; model/retrieval/storage remain separate."""
import json
import os
import re
import time
from urllib.parse import urlsplit, urldefrag

import requests
from bs4 import BeautifulSoup
from jsonschema import validate


def public_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Use an explicit public HTTPS source you may access.")
    if parsed.port not in (None, 443) or parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Not a public HTTPS source.")
    return urldefrag(url)[0]


def envelope(response):
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict) or data.get("success") is not True or "result" not in data:
        raise RuntimeError("Browser Run returned an unsuccessful or malformed envelope.")
    return data["result"]


class BrowserRun:
    def __init__(self, account_id=None, token=None, session=None):
        self.account_id = account_id or os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
        self.token = token or os.environ.get("CLOUDFLARE_API_TOKEN", "")
        if not re.fullmatch(r"[a-fA-F0-9]{32}", self.account_id) or not self.token:
            raise ValueError("Configure CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN locally.")
        self.base = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/browser-run"
        self.session = session or requests.Session()

    def request(self, method, endpoint, *, payload=None, params=None):
        if not re.fullmatch(r"(?:content|markdown|json|scrape|links|crawl)(?:/[a-zA-Z0-9-]+)?", endpoint):
            raise ValueError("Unsupported acquisition endpoint.")
        return envelope(self.session.request(method, f"{self.base}/{endpoint}",
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            json=payload, params=params, timeout=(10, 90), allow_redirects=False))

    def extract(self, endpoint, url, **options):
        url = public_url(url)
        # This tutorial intentionally limits acquisition to the source documentation/blog.
        if urlsplit(url).hostname not in {"developers.cloudflare.com", "blog.cloudflare.com", "example.com"}:
            raise ValueError("Source origin is not in this tutorial's allow-list.")
        result = self.request("POST", endpoint, payload={"url": url, **options})
        if endpoint in {"content", "markdown"} and not isinstance(result, str):
            raise TypeError("Expected text acquisition result.")
        return result

    def json(self, url, prompt, schema):
        value = self.extract("json", url, prompt=prompt,
            response_format={"type": "json_schema", "json_schema": schema})
        if isinstance(value, str):
            value = json.loads(value)
        validate(value, schema)
        return value

    def crawl(self, url, *, attempts=30, delay=5, sleep=time.sleep):
        if type(attempts) is not int or not 1 <= attempts <= 60 or not 0 <= delay <= 30:
            raise ValueError("Use bounded polling limits.")
        job = self.extract("crawl", url, limit=10, depth=2, formats=["markdown"],
            options={"includeExternalLinks": False, "includeSubdomains": False},
            crawlPurposes=["ai-input"], contentUse="full")
        job_id = job.get("id") if isinstance(job, dict) else job
        if not isinstance(job_id, str) or not re.fullmatch(r"[a-zA-Z0-9-]+", job_id):
            raise ValueError("Invalid crawl identifier.")
        for index in range(attempts):
            state = self.request("GET", f"crawl/{job_id}", params={"limit": 1})
            status = state.get("status") if isinstance(state, dict) else None
            if status == "completed":
                break
            if status not in {"running", "queued"}:
                raise RuntimeError(f"Crawl did not complete: {status!r}")
            if index + 1 < attempts:
                sleep(delay)
        else:
            # Client timeout is not server cancellation. Return its ID for explicit follow-up.
            raise TimeoutError(f"Crawl {job_id} remains pending; inspect or cancel it explicitly.")
        records = [];cursor = None;seen = set()
        for _ in range(20):
            params = {"limit": 10, "status": "completed"}
            if cursor is not None:
                params["cursor"] = cursor
            page = self.request("GET", f"crawl/{job_id}", params=params)
            if not isinstance(page, dict) or page.get("status") != "completed" or not isinstance(page.get("records"), list):
                raise RuntimeError("Invalid completed crawl page.")
            records.extend(page["records"])
            cursor = page.get("cursor")
            if cursor is None:
                return records
            if str(cursor) in seen:
                raise RuntimeError("Repeated crawl cursor.")
            seen.add(str(cursor))
        raise RuntimeError("Crawl pagination limit reached.")


def main_text(html):
    soup = BeautifulSoup(html, "html.parser")
    node = soup.find("main") or soup.find("article") or soup
    for child in node.select("script,style,nav,footer,header"):
        child.decompose()
    return node.get_text(" ", strip=True)


def markdown_sections(markdown):
    """Split ATX headings outside backtick/tilde code fences."""
    result = [];lines = [];fence = None
    for line in markdown.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line.strip().strip(marker[0]):
                fence = None
        if fence is None and re.match(r"^ {0,3}#{1,6}\s+", line) and lines:
            result.append("\n".join(lines).strip());lines = []
        lines.append(line)
    if lines:
        result.append("\n".join(lines).strip())
    return [section for section in result if section]


def same_origin_links(links, origin):
    if not isinstance(links, list) or not all(isinstance(x, str) for x in links):
        raise TypeError("Expected a list of URL strings.")
    expected = urlsplit(public_url(origin)).netloc
    result = []
    for link in links:
        try:
            value = public_url(link)
        except ValueError:
            continue
        if urlsplit(value).netloc == expected and value not in result:
            result.append(value)
    return result
