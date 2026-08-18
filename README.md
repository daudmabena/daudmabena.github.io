# daudmabena.github.io

Personal portfolio site for Daud Mabena, published with GitHub Pages at
[daudmabena.github.io](https://daudmabena.github.io). It lists my public
repositories and short technical write-ups.

<!--
  Add a screenshot here once you have one: capture the site at 1440px wide, save
  it as docs/screenshots/home.png, and reference it with a relative path. Leaving
  a broken image tag in place is worse than having no screenshot, so this is a
  comment until the file exists.
-->

## About this site

A static site generated from a [gitfolio](https://github.com/imfunniee/gitfolio)
template and then customised by hand. The generator reads `config.json`, pulls
public repository data from the GitHub API, and writes plain HTML. There is no
build step and no framework at runtime, which is the reason the site still works
years after it was generated.

## Stack

| Part | Detail |
| --- | --- |
| Output | Static HTML and CSS, no build step |
| Hosting | GitHub Pages, served from the repository root |
| Layout | [magic-grid](https://github.com/e-oj/Magic-Grid) for the masonry project grid |
| Other | jQuery, animate.css, Font Awesome, Google Fonts, all from CDNs |

## Structure

```
index.html            The full site, with repository cards rendered into the markup
index.css             Styles, including the light and dark colour variables
config.json           Original gitfolio configuration: username, display name, sort order
blog/                 One directory per write-up, each containing an index.html
dist/                 Original generator output, kept as a reference copy
tools/
  update_site.py      Refreshes the project cards from the GitHub API
  site.config.json    Which repositories appear, and in what order
.github/workflows/
  update-site.yml     Runs the refresh weekly, and on demand
```

The site is served from the repository root, so `index.html` there is the live
page. `dist/` holds the files as gitfolio originally produced them.

## Keeping the project cards current

The card list is part of `index.html` rather than fetched at page load, so it
does not update on its own, and re-running gitfolio would discard the hand edits
made since. `tools/update_site.py` solves that by rewriting only the card list:

```bash
python3 tools/update_site.py --check   # report what would change, write nothing
python3 tools/update_site.py           # rewrite index.html if anything changed
```

It needs only Python 3 — no dependencies. Set `GITHUB_TOKEN` to raise the API
rate limit from 60 requests an hour to 5000; without it a single run still fits
inside the unauthenticated limit.

Which repositories appear is controlled by `tools/site.config.json`: forks are
excluded, `exclude` lists repositories to leave off with a reason for each, and
`extra` pulls in repositories from outside the account. Cards are ordered by most
recently pushed, so current work appears first.

The **Update site** workflow runs this weekly and can be triggered from the
Actions tab. It commits only when the card list has actually changed.

A repository with no description renders as a card with the description line
hidden. Adding a description on GitHub is the fix; it needs no change here.

## Running it locally

No dependencies are required. Any static file server will do, because the page
fetches `blog.json` over HTTP and will not work correctly from a `file://` URL:

```bash
git clone https://github.com/daudmabena/daudmabena.github.io.git
cd daudmabena.github.io
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Making changes

- **Content and styling** — edit `index.html` and `index.css` directly. Changes
  pushed to the default branch are published by GitHub Pages within a minute or two.
- **Adding a write-up** — create `blog/<url-title>/index.html` following the
  existing post as a model.
- **Regenerating from the template** — running the generator again overwrites
  `index.html` and discards any hand edits, so keep customisations noted before
  doing it.

## Known limitations

- Several cards show no description or language because the underlying
  repositories have none set on GitHub.
- Third-party assets load from CDNs, so the page depends on those staying
  available.
- The page is built on jQuery and a masonry layout script from the original
  template, and logs some deprecation warnings in the browser console. They are
  cosmetic and predate the current content.

## Licence

Site content is mine. The underlying template is
[gitfolio](https://github.com/imfunniee/gitfolio) by
[@imfunniee](https://github.com/imfunniee), used under its own licence.
