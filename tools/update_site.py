#!/usr/bin/env python3
"""Refresh the generated regions of index.html from the GitHub API.

Four regions of the page are generated, each delimited by HTML comment markers:

    FEATURED  project drawings for the repositories listed in "featured"
    REVS      revision history, from real public repository activity
    METRICS   measured values and language distribution
    REPOS     index of every non-fork public repository not excluded

Everything outside those markers is hand-written and left untouched, so the
design can be edited freely without this script fighting it.

Descriptions, topics, languages and dates come from GitHub. Nothing is invented:
a featured repository with no description on GitHub is skipped with a warning
rather than published with placeholder text, and the revision history reports
counted activity rather than a narrative.

Standard library only, so CI needs no install step.

Usage:
    python3 tools/update_site.py           # rewrite index.html if anything changed
    python3 tools/update_site.py --check    # report what would change, write nothing
"""

from __future__ import annotations

import collections
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

REGIONS = {
    "featured": ("<!-- FEATURED:START -->", "<!-- FEATURED:END -->"),
    "revs": ("<!-- REVS:START -->", "<!-- REVS:END -->"),
    "metrics": ("<!-- METRICS:START -->", "<!-- METRICS:END -->"),
    "repos": ("<!-- REPOS:START -->", "<!-- REPOS:END -->"),
}


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


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

IND = " " * 10  # matches the indentation of the marker comments in index.html


def render_project(repo: dict, index: int, architecture: dict) -> str:
    """A project as an engineering drawing: title strip, body, architecture stack."""
    ref = f"SYS-{index:03d}"
    description = escape(repo["description"])
    homepage = (repo.get("homepage") or "").strip()
    topics = (repo.get("topics") or [])[:8]
    language = repo.get("language")

    # "Active" is derived from the last push year rather than asserted.
    pushed_year = (repo.get("pushed_at") or "")[:4]
    is_active = pushed_year >= "2025"
    status = "Active" if is_active else f"Last revised {pushed_year}"

    topic_block = ""
    if topics:
        items = "".join(f"<li>{escape(t)}</li>" for t in topics)
        topic_block = f'\n                <ul class="project__topics">{items}</ul>'

    demo = (
        f'\n                  <a class="btn" href="{escape(homepage)}" target="_blank" '
        f'rel="noopener">Live demo</a>'
        if homepage
        else ""
    )

    # Architecture rows come from config, which records only what the repository's
    # own metadata supports. With none recorded, the panel states that plainly
    # rather than showing invented layers.
    rows = architecture.get(repo["name"]) or {}
    if rows:
        layers = []
        for position, (label, value) in enumerate(rows.items()):
            if position:
                layers.append(f'{IND}          <span class="arch-join" aria-hidden="true"></span>')
            layers.append(
                f'{IND}          <div class="arch-layer">\n'
                f'{IND}            <p class="arch-layer__label">{escape(label)}</p>\n'
                f'{IND}            <p class="arch-layer__value">{escape(value)}</p>\n'
                f"{IND}          </div>"
            )
        arch_body = (
            f'{IND}        <div class="arch-stack">\n' + "\n".join(layers) + f"\n{IND}        </div>"
        )
    else:
        arch_body = (
            f'{IND}        <p class="ref" style="margin-top:0.8rem">Not yet documented '
            f"&mdash; add rows for this repository under &quot;architecture&quot; in "
            f"tools/site.config.json.</p>"
        )

    language_row = (
        f'\n              <span class="callout">Primary language: {escape(language)}</span>'
        if language
        else ""
    )

    return f"""{IND}  <article class="project panel ink-frame">
{IND}    <header class="project__head">
{IND}      <span class="project__id">{ref}</span>
{IND}      <h3 class="project__name">
{IND}        <a href="{escape(repo['html_url'])}" target="_blank" rel="noopener">{escape(repo['name'])}</a>
{IND}      </h3>
{IND}      <span class="project__status" data-status="{'active' if is_active else 'archive'}">{escape(status)}</span>
{IND}    </header>

{IND}    <div class="project__body">
{IND}      <div class="project__main">
{IND}        <p class="project__desc">{description}</p>{topic_block}{language_row}
{IND}        <div class="project__links">
{IND}          <a class="btn" href="{escape(repo['html_url'])}" target="_blank" rel="noopener">Repository</a>{demo}
{IND}        </div>
{IND}      </div>

{IND}      <div class="project__arch">
{IND}        <p class="label">Architecture</p>
{arch_body}
{IND}      </div>
{IND}    </div>
{IND}  </article>"""


def render_repo(repo: dict, index: int) -> str:
    """A compact card for the repository index."""
    description = repo.get("description")
    language = repo.get("language")

    description_block = (
        f'\n            <p class="repo__desc">{escape(description)}</p>'
        if description
        else ""
    )
    language_item = (
        f'\n              <li data-lang="{escape(language)}">'
        f'<span class="dot"></span>{escape(language)}</li>'
        if language
        else ""
    )

    return f"""{IND}  <a class="repo" href="{escape(repo['html_url'])}" target="_blank" rel="noopener">
{IND}    <span class="repo__top">
{IND}      <span class="repo__no">{index:02d}</span>
{IND}      <span class="repo__name">{escape(repo['name'])}</span>
{IND}    </span>{description_block}
{IND}    <ul class="repo__meta">{language_item}
{IND}      <li>{STAR_ICON}{repo.get('stargazers_count', 0)}</li>
{IND}      <li>{FORK_ICON}{repo.get('forks_count', 0)}</li>
{IND}    </ul>
{IND}  </a>"""


def render_metrics(selected: list[dict], own: list[dict]) -> str:
    """Measured values, all counted rather than asserted."""
    languages = collections.Counter(r["language"] for r in own if r.get("language"))
    stars = sum(r.get("stargazers_count", 0) for r in own)
    years = [r["pushed_at"][:4] for r in own if r.get("pushed_at")]
    first_year = min((r["created_at"][:4] for r in own if r.get("created_at")), default="—")
    latest = max(years) if years else "—"

    gauges = [
        (str(len(own)), "", "Repositories authored"),
        (str(len(languages)), "", "Languages in use"),
        (first_year, "", "First public commit"),
        (latest, "", "Most recent activity"),
        (str(stars), "", "Stars received"),
    ]

    gauge_html = "\n".join(
        f'{IND}    <div class="gauge">\n'
        f'{IND}      <p class="gauge__value">{escape(value)}'
        f'{f"<span class=gauge__unit>{escape(unit)}</span>" if unit else ""}</p>\n'
        f'{IND}      <p class="label gauge__label">{escape(label)}</p>\n'
        f"{IND}    </div>"
        for value, unit, label in gauges
    )

    total = sum(languages.values()) or 1
    segments = "".join(
        f'<span class="dist__seg" data-lang="{escape(lang)}" '
        f'style="width:{count / total * 100:.2f}%" title="{escape(lang)}: {count}"></span>'
        for lang, count in languages.most_common()
    )
    keys = "\n".join(
        f'{IND}        <li data-lang="{escape(lang)}"><span class="swatch"></span>'
        f"{escape(lang)} <b>{count / total * 100:.0f}%</b></li>"
        for lang, count in languages.most_common()
    )

    return f"""{IND}  <div class="gauges">
{gauge_html}
{IND}  </div>

{IND}  <div class="dist ink-frame">
{IND}    <div class="dist__head">
{IND}      <span class="smark" aria-hidden="true">B</span>
{IND}      <span class="label">Language distribution &mdash; by repository count</span>
{IND}      <span class="panel__ref" style="margin-left:auto">MEA-002</span>
{IND}    </div>
{IND}    <div class="dist__body">
{IND}      <div class="dist__bar" role="img" aria-label="Language distribution across {len(own)} repositories">{segments}</div>
{IND}      <ul class="dist__key">
{keys}
{IND}      </ul>
{IND}    </div>
{IND}  </div>"""


def render_revisions(own: list[dict], timeline: list[dict]) -> str:
    """Revision history.

    Professional roles come from config when present. The derived log below them
    counts real repository activity per year and makes no claim about employment.
    """
    head = (
        f'{IND}    <div class="revs__head">\n'
        f'{IND}      <span class="label">Rev</span>\n'
        f'{IND}      <span class="label">Period</span>\n'
        f'{IND}      <span class="label">Record</span>\n'
        f'{IND}      <span class="label">Detail</span>\n'
        f"{IND}    </div>"
    )

    blocks = []

    if timeline:
        rows = "\n".join(
            f'{IND}    <div class="rev">\n'
            f'{IND}      <span class="rev__no">Rev {escape(str(entry.get("rev", "")))}</span>\n'
            f'{IND}      <span class="rev__period">{escape(str(entry.get("period", "")))}</span>\n'
            f'{IND}      <span class="rev__title">{escape(str(entry.get("title", "")))}</span>\n'
            f'{IND}      <span class="rev__detail">{escape(str(entry.get("detail", "")))}</span>\n'
            f"{IND}    </div>"
            for entry in timeline
        )
        blocks.append(
            f'{IND}  <p class="section__note">Professional record.</p>\n'
            f'{IND}  <div class="revs">\n{head}\n{rows}\n{IND}  </div>'
        )

    # Derived log: one row per year that had activity, newest first.
    by_year: dict[str, list[dict]] = collections.defaultdict(list)
    for repo in own:
        if repo.get("pushed_at"):
            by_year[repo["pushed_at"][:4]].append(repo)

    rows = []
    for position, year in enumerate(sorted(by_year, reverse=True)):
        repos = by_year[year]
        languages = sorted({r["language"] for r in repos if r.get("language")})
        rows.append(
            f'{IND}    <div class="rev">\n'
            f'{IND}      <span class="rev__no">Rev {len(by_year) - position:02d}</span>\n'
            f'{IND}      <span class="rev__period">{year}</span>\n'
            f'{IND}      <span class="rev__title">{len(repos)} '
            f'{"repository" if len(repos) == 1 else "repositories"} revised</span>\n'
            f'{IND}      <span class="rev__detail">{escape(", ".join(languages) or "no language detected")}</span>\n'
            f"{IND}    </div>"
        )

    blocks.append(
        f'{IND}  <p class="section__note">Derived from public repository history: the '
        f"year each repository was last pushed to, and the languages involved. This is "
        f"an activity record, not an employment history &mdash; professional roles are "
        f"not published here.</p>\n"
        f'{IND}  <div class="revs">\n{head}\n' + "\n".join(rows) + f"\n{IND}  </div>"
    )

    return "\n\n".join(blocks)


def replace_region(html: str, name: str, body: str) -> str:
    start_marker, end_marker = REGIONS[name]
    if start_marker not in html or end_marker not in html:
        raise SystemExit(
            f"Could not find {start_marker} / {end_marker} in index.html. "
            f"The generated regions must keep their marker comments."
        )

    start = html.index(start_marker) + len(start_marker)
    end = html.index(end_marker)
    if end < start:
        raise SystemExit(f"{end_marker} appears before {start_marker} in index.html")

    return f"{html[:start]}\n{body}\n{IND}{html[end:]}"


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
    by_full_name = {repo["full_name"]: repo for repo in repos}
    all_repos = list(by_full_name.values())

    selected, counts = select(all_repos, config)
    if not selected:
        raise SystemExit("No repositories selected; refusing to publish an empty list.")

    # Metrics count everything authored here, before the presentation excludes.
    own = [r for r in all_repos if not r.get("fork")]

    lookup = {repo["name"]: repo for repo in all_repos}
    featured: list[dict] = []
    for name in config.get("featured") or []:
        repo = lookup.get(name)
        if repo is None:
            warn(f'featured repository "{name}" was not found; skipping it.')
            continue
        if not repo.get("description"):
            warn(
                f'featured repository "{name}" has no description on GitHub, so it '
                f"cannot be shown as a project drawing. Add one on GitHub, then run "
                f"this again."
            )
            continue
        featured.append(repo)

    print(f"{counts['total']} repositories fetched for {username}")
    print(f"  {counts['forks']} forks skipped")
    print(f"  {counts['excluded']} excluded by config")
    print(f"  {counts['archived']} archived skipped")
    print(f"  {len(own)} authored here (metrics basis)")
    print(f"  {len(featured)} featured, {len(selected)} indexed\n")

    original = INDEX_PATH.read_text()
    updated = original

    architecture = config.get("architecture") or {}
    if featured:
        cards = "\n\n".join(
            render_project(repo, position, architecture)
            for position, repo in enumerate(featured, start=1)
        )
        body = f'{IND}<div class="projects">\n{cards}\n{IND}</div>'
        for repo in featured:
            if repo["name"] not in architecture:
                warn(
                    f'no architecture rows recorded for featured project "{repo["name"]}"; '
                    f"its architecture panel will say so."
                )
    else:
        warn("no featured projects resolved; that section will be empty.")
        body = ""
    updated = replace_region(updated, "featured", body)

    updated = replace_region(
        updated, "revs", render_revisions(own, config.get("timeline") or [])
    )
    updated = replace_region(updated, "metrics", render_metrics(selected, own))

    grid = "\n".join(
        render_repo(repo, position) for position, repo in enumerate(selected, start=1)
    )
    updated = replace_region(updated, "repos", f'{IND}<div class="repos">\n{grid}\n{IND}</div>')

    undescribed = [r["name"] for r in selected if not r.get("description")]
    if undescribed:
        print(
            f"{len(undescribed)} indexed repositories have no description, so they "
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
