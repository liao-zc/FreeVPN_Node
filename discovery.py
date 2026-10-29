"""Discover subscription artifacts from GitHub repositories pushed in the last week."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
import re
import urllib.parse
import urllib.request

API = "https://api.github.com"
UA = "FreeVPN-Node-Aggregator/1.0"


def discover_recent_entries(timeout: int = 15, max_repositories: int = 20) -> tuple[list[dict[str, str | int]], list[str]]:
    """Return raw repo feed links plus Telegram previews for the collector."""
    cutoff = (datetime.now(timezone.utc).date() - timedelta(days=7)).isoformat()
    query = urllib.parse.urlencode({
        "q": f'(v2ray OR clash OR proxy) stars:>300 pushed:>={cutoff}',
        "sort": "stars", "order": "desc", "per_page": "50",
    })
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    def get_json(url: str) -> dict:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read(3 * 1024 * 1024).decode("utf-8"))

    try:
        result = get_json(f"{API}/search/repositories?{query}")
    except Exception as exc:
        print(f"GitHub repository search skipped: {type(exc).__name__}: {exc}")
        return [], []

    entries: list[dict[str, str | int]] = []
    telegram: list[str] = []
    seen_urls: set[str] = set()
    for repo in result.get("items", [])[:max_repositories]:
        full_name = repo.get("full_name", "")
        branch = repo.get("default_branch", "main")
        if not full_name or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", full_name):
            continue
        tree_url = f"{API}/repos/{full_name}/git/trees/{urllib.parse.quote(branch, safe='')}?recursive=1"
        try:
            tree = get_json(tree_url)
        except Exception as exc:
            print(f"GitHub tree skipped for {full_name}: {type(exc).__name__}: {exc}")
            continue

        paths = []
        for item in tree.get("tree", []):
            path = str(item.get("path", ""))
            lower = path.lower()
            if item.get("type") != "blob" or int(item.get("size", 5 * 1024 * 1024 + 1)) > 5 * 1024 * 1024:
                continue
            if not lower.endswith((".txt", ".yaml", ".yml", ".json")):
                continue
            if not re.search(r"(^|[/_.-])(sub(?:scription)?s?|clash|v2ray|nodes?|proxies|proxy|output)([/_.-]|$)", lower):
                continue
            if any(word in lower for word in ("readme", "workflow", "example", "template", "source")):
                continue
            paths.append(path)
        paths.sort(key=lambda path: (not any(term in path.lower() for term in ("subscription", "sub", "clash", "v2ray")), len(path)))
        added = 0
        for path in paths[:3]:
            url = f"https://raw.githubusercontent.com/{full_name}/{urllib.parse.quote(branch, safe='')}/{urllib.parse.quote(path, safe='/')}"
            if url in seen_urls:
                continue
            entries.append({
                "repo": full_name,
                "repo_url": f"https://github.com/{full_name}",
                "updated_at": str(repo.get("pushed_at", ""))[:10],
                "stars": int(repo.get("stargazers_count", 0)),
                "url": url,
            })
            seen_urls.add(url)
            added += 1
        print(f"GitHub discovery: {full_name} ({repo.get('stargazers_count', 0)} stars), {added} feed candidates")

        readme_url = f"https://raw.githubusercontent.com/{full_name}/{urllib.parse.quote(branch, safe='')}/README.md"
        try:
            request = urllib.request.Request(readme_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                readme = response.read(512 * 1024).decode("utf-8", errors="replace")
            channels = sorted(set(re.findall(r"(?:https?://)?t\.me/(?:s/)?([A-Za-z0-9_]{5,})", readme, flags=re.I)))
            channels = [name for name in channels if name.lower() not in {"share", "joinchat", "addstickers", "proxy", "socks"}]
            telegram.extend(f"https://t.me/s/{name}" for name in channels[:3])
            if channels[:3]:
                print(f"GitHub discovery: {full_name}, {min(3, len(channels))} public Telegram previews")
        except Exception:
            pass
    print(f"GitHub discovery added {len(entries)} repository feeds and {len(telegram)} Telegram previews")
    return entries, telegram
