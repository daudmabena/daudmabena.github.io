#!/usr/bin/env python3
"""Refresh the project cards in index.html from the GitHub API.

The site was originally produced by gitfolio, which bakes repository data into
the HTML at generation time. That means stars, forks, descriptions, and any new
repository go stale the moment the file is written, and re-running the original
generator would overwrite the hand edits made since. This script updates only
the card list, leaving the rest of the page alone.

Reads tools/site.config.json. Standard library only, so CI needs no install step.

Usage:
    python3 tools/update_site.py           # rewrite index.html if anything changed
    python3 tools/update_site.py --check    # report what would change, write nothing
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "tools" / "site.config.json"
INDEX_PATH = ROOT / "index.html"

# The card list sits between these two markers in index.html. If the surrounding
# markup is ever restructured, the script fails loudly rather than writing a
# corrupted page.
SECTION_START = '<div class="projects" id="work_section">'
SECTION_END_ANCHOR = '\n      </div>\n      <div id="forks"'

API = "https://api.github.com"


def api_get(path: str, optional: bool = False) -> object:
    """Fetch a single API path. With optional=True, a 404 returns None instead of exiting."""
    request = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "daudmabena-site-updater",
        },
    )
    # Unauthenticated requests are limited to 60 an hour, which one full run can
    # exceed. The workflow passes the automatic token, which raises it to 5000.
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if optional and error.code == 404:
            return None
        detail = error.read().decode("utf-8", "replace")[:200]
        raise SystemExit(f"GitHub API {error.code} for {path}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not reach the GitHub API: {error.reason}") from error


def fetch_user_repos(username: str) -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        batch = api_get(f"/users/{username}/repos?per_page=100&page={page}")
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        page += 1
        if page > 20:  # ~2000 repositories; a guard against an unbounded loop
            break
    return repos


def fetch_named_repos(full_names: list[str]) -> list[dict]:
    """Fetch repositories outside the user account, such as organisation ones.

    A listed repository that has been made private or deleted is skipped with a
    warning: it should not take the whole site update down, and continuing keeps
    a dead card off the page.
    """
    found = []
    for full_name in full_names:
        repo = api_get(f"/repos/{full_name}", optional=True)
        if isinstance(repo, dict) and repo.get("name"):
            found.append(repo)
        else:
            print(
                f"warning: {full_name} is not publicly available (private or deleted), "
                f"so it is being left off the site. Remove it from the "
                f'"extra" list in tools/site.config.json to silence this.',
                file=sys.stderr,
            )
    return found


def select(repos: list[dict], config: dict) -> tuple[list[dict], dict[str, int]]:
    excluded = config.get("exclude") or {}
    include_forks = bool(config.get("include_forks"))

    counts = {"total": len(repos), "forks": 0, "excluded": 0, "archived": 0}
    kept = []
    for repo in repos:
        if repo.get("fork") and not include_forks:
            counts["forks"] += 1
            continue
        if repo.get("name") in excluded:
            counts["excluded"] += 1
            continue
        if repo.get("archived"):
            counts["archived"] += 1
            continue
        kept.append(repo)

    key = {
        "pushed": "pushed_at",
        "updated": "updated_at",
        "created": "created_at",
        "stars": "stargazers_count",
        "name": "name",
    }.get(config.get("sort", "pushed"), "pushed_at")
    kept.sort(key=lambda r: r.get(key) or "", reverse=config.get("order", "desc") == "desc")
    return kept, counts


def render_card(repo: dict) -> str:
    """Reproduce the existing card markup exactly, so the styling still applies."""
    description = repo.get("description")
    language = repo.get("language")

    description_style = "display:block;" if description else "display:none;"
    description_text = escape(description) if description else "undefined"
    language_style = "display:inline-block;" if language else "display:none;"
    language_text = escape(language) if language else "null"

    return f"""                        <a href="{escape(repo['html_url'])}" target="_blank">
                        <section>
                            <div class="section_title">{escape(repo['name'])}</div>
                            <div class="about_section">
                            <span style="{description_style}">{description_text}</span>
                            </div>
                            <div class="bottom_section">
                                <span style="{language_style}"><i class="fas fa-code"></i>&nbsp; {language_text}</span>
                                <span><i class="fas fa-star"></i>&nbsp; {repo.get('stargazers_count', 0)}</span>
                                <span><i class="fas fa-code-branch"></i>&nbsp; {repo.get('forks_count', 0)}</span>
                            </div>
                        </section>
                        </a>"""


def splice(html: str, cards: str) -> str:
    if SECTION_START not in html:
        raise SystemExit(f"Could not find {SECTION_START!r} in index.html")
    if SECTION_END_ANCHOR not in html:
        raise SystemExit("Could not find the end of the project list in index.html")

    start = html.index(SECTION_START) + len(SECTION_START)
    end = html.index(SECTION_END_ANCHOR)
    if end <= start:
        raise SystemExit("The project list markers in index.html are out of order")

    replaced = html[start:end]
    if not replaced.rstrip().endswith("</div>"):
        raise SystemExit(
            "Refusing to write: the project list does not end where expected. "
            "Check whether index.html has been restructured."
        )

    return f"{html[:start]}\n{cards}</div>{html[end:]}"


def main() -> int:
    check_only = "--check" in sys.argv

    config = json.loads(CONFIG_PATH.read_text())
    username = config["username"]

    repos = fetch_user_repos(username)
    repos.extend(fetch_named_repos(config.get("extra") or []))

    # An "extra" entry may duplicate one already returned for the user.
    unique = {repo["full_name"]: repo for repo in repos}
    selected, counts = select(list(unique.values()), config)

    if not selected:
        raise SystemExit("No repositories selected; refusing to publish an empty list.")

    cards = "\n".join(render_card(repo) for repo in selected)
    original = INDEX_PATH.read_text()
    updated = splice(original, cards)

    print(f"{counts['total']} repositories fetched for {username}")
    print(f"  {counts['forks']} forks skipped")
    print(f"  {counts['excluded']} excluded by config")
    print(f"  {counts['archived']} archived skipped")
    print(f"  {len(selected)} shown on the site\n")

    print("Shown, in page order:")
    for repo in selected:
        stars = repo.get("stargazers_count", 0)
        print(
            f"  {repo['name'][:34]:34} {str(repo.get('language'))[:12]:12} "
            f"{'*' + str(stars) if stars else '':4} {repo.get('pushed_at', '')[:10]}"
        )
    print()

    undescribed = [r["name"] for r in selected if not r.get("description")]
    if undescribed:
        print(
            f"{len(undescribed)} of these have no description, so they render as bare "
            f"cards: {', '.join(undescribed)}"
        )
        print("Adding a description on GitHub is the fix; it needs no code change.\n")

    if updated == original:
        print("index.html is already up to date.")
        return 0

    if check_only:
        print("index.html would change (running with --check, nothing written).")
        return 1

    INDEX_PATH.write_text(updated)
    print("index.html updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
