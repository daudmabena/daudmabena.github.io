#!/usr/bin/env python3
"""Refresh the generated sections of index.html from the GitHub API.

Two regions of the page are generated, each delimited by HTML comment markers:

    FEATURED  selected projects, listed in tools/site.config.json
    REPOS     every non-fork public repository not excluded by config

Everything outside those markers is hand-written and left untouched, so the
design can be edited freely without this script fighting it.

Descriptions and topics are taken verbatim from GitHub. Nothing is invented
here: a featured repository with no description on GitHub is skipped with a
warning rather than published with placeholder text.

Standard library only, so CI needs no install step.

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

API = "https://api.github.com"

FEATURED_MARKERS = ("<!-- FEATURED:START -->", "<!-- FEATURED:END -->")
REPOS_MARKERS = ("<!-- REPOS:START -->", "<!-- REPOS:END -->")


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #


def api_get(path: str, optional: bool = False) -> object:
    """Fetch a single API path. With optional=True, a 404 returns None."""
    request = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "daudmabena-site-updater",
        },
    )
    # Unauthenticated requests are limited to 60 an hour, which a full run can
    # exceed. The workflow passes the automatic token, raising it to 5000.
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

    One that has been made private or deleted is skipped with a warning: it
    should not take the whole update down, and skipping keeps a dead card off
    the page.
    """
    found = []
    for full_name in full_names:
        repo = api_get(f"/repos/{full_name}", optional=True)
        if isinstance(repo, dict) and repo.get("name"):
            found.append(repo)
        else:
            warn(
                f"{full_name} is not publicly available (private or deleted), so it "
                f'is being left off the site. Remove it from "extra" in '
                f"tools/site.config.json to silence this."
            )
    return found


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Selection
# --------------------------------------------------------------------------- #


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


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

STAR_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M12 3.5l2.6 5.3 5.9.9-4.2 4.1 1 5.8-5.3-2.8-5.3 2.8 1-5.8L3.5 9.7l5.9-.9z"/>'
    "</svg>"
)
FORK_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="5" r="2"/>'
    '<circle cx="12" cy="19" r="2"/><path d="M6 7v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V7M12 13v4"/>'
    "</svg>"
)


def render_featured(repo: dict) -> str:
    """A large card for a selected project, using its own GitHub description."""
    description = escape(repo["description"])
    language = repo.get("language")
    homepage = (repo.get("homepage") or "").strip()
    topics = (repo.get("topics") or [])[:6]

    topic_items = "".join(f"<li>{escape(t)}</li>" for t in topics)
    topic_block = (
        f'\n              <ul class="project__topics">{topic_items}</ul>'
        if topic_items
        else ""
    )

    language_block = (
        f'\n                <li class="repo__lang" data-lang="{escape(language)}">'
        f'<span class="dot"></span>{escape(language)}</li>'
        if language
        else ""
    )

    demo_link = (
        f'\n                <a class="btn" href="{escape(homepage)}" target="_blank" '
        f'rel="noopener">Live</a>'
        if homepage
        else ""
    )

    return f"""            <li class="project">
              <div>
                <div class="project__head">
                  <h3 class="project__name">
                    <a href="{escape(repo['html_url'])}" target="_blank" rel="noopener">{escape(repo['name'])}</a>
                  </h3>
                </div>
                <p class="project__desc">{description}</p>{topic_block}
              </div>
              <div class="project__side">
                <ul class="repo__meta">{language_block}
                  <li>{STAR_ICON}{repo.get('stargazers_count', 0)}</li>
                </ul>
                <div class="project__links">
                  <a class="btn" href="{escape(repo['html_url'])}" target="_blank" rel="noopener">Code</a>{demo_link}
                </div>
              </div>
            </li>"""


def render_repo(repo: dict) -> str:
    """A compact card for the full repository list."""
    description = repo.get("description")
    language = repo.get("language")

    description_block = (
        f'\n            <p class="repo__desc">{escape(description)}</p>'
        if description
        else ""
    )
    language_block = (
        f'\n              <li class="repo__lang" data-lang="{escape(language)}">'
        f'<span class="dot"></span>{escape(language)}</li>'
        if language
        else ""
    )

    return f"""          <a class="repo" href="{escape(repo['html_url'])}" target="_blank" rel="noopener">
            <h3 class="repo__name">{escape(repo['name'])}</h3>{description_block}
            <ul class="repo__meta">{language_block}
              <li>{STAR_ICON}{repo.get('stargazers_count', 0)}</li>
              <li>{FORK_ICON}{repo.get('forks_count', 0)}</li>
            </ul>
          </a>"""


def replace_region(html: str, markers: tuple[str, str], body: str) -> str:
    start_marker, end_marker = markers
    if start_marker not in html or end_marker not in html:
        raise SystemExit(
            f"Could not find {start_marker} / {end_marker} in index.html. "
            f"The generated regions must keep their marker comments."
        )

    start = html.index(start_marker) + len(start_marker)
    end = html.index(end_marker)
    if end < start:
        raise SystemExit(f"{end_marker} appears before {start_marker} in index.html")

    return f"{html[:start]}\n{body}\n          {html[end:]}"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    check_only = "--check" in sys.argv

    config = json.loads(CONFIG_PATH.read_text())
    username = config["username"]

    repos = fetch_user_repos(username)
    repos.extend(fetch_named_repos(config.get("extra") or []))

    # An "extra" entry may duplicate one already returned for the user.
    by_name = {repo["full_name"]: repo for repo in repos}
    selected, counts = select(list(by_name.values()), config)

    if not selected:
        raise SystemExit("No repositories selected; refusing to publish an empty list.")

    # --- featured -------------------------------------------------------- #
    lookup = {repo["name"]: repo for repo in by_name.values()}
    featured: list[dict] = []
    for name in config.get("featured") or []:
        repo = lookup.get(name)
        if repo is None:
            warn(f'featured repository "{name}" was not found; skipping it.')
            continue
        if not repo.get("description"):
            warn(
                f'featured repository "{name}" has no description on GitHub, so it '
                f"cannot be shown as a selected project. Add one on GitHub, then "
                f"run this again."
            )
            continue
        featured.append(repo)

    print(f"{counts['total']} repositories fetched for {username}")
    print(f"  {counts['forks']} forks skipped")
    print(f"  {counts['excluded']} excluded by config")
    print(f"  {counts['archived']} archived skipped")
    print(f"  {len(featured)} featured, {len(selected)} listed\n")

    if featured:
        print("Featured:")
        for repo in featured:
            print(f"  {repo['name']}")
        print()

    original = INDEX_PATH.read_text()
    updated = original

    if featured:
        cards = "\n".join(render_featured(repo) for repo in featured)
        body = f'          <ul class="featured">\n{cards}\n          </ul>'
    else:
        warn("no featured projects resolved; that section will be empty.")
        body = ""
    updated = replace_region(updated, FEATURED_MARKERS, body)

    grid = "\n".join(render_repo(repo) for repo in selected)
    updated = replace_region(
        updated, REPOS_MARKERS, f'        <div class="repos">\n{grid}\n        </div>'
    )

    undescribed = [r["name"] for r in selected if not r.get("description")]
    if undescribed:
        print(
            f"{len(undescribed)} listed repositories have no description, so they "
            f"render as name-only cards:\n  {', '.join(undescribed)}"
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
