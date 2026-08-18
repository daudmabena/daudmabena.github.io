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
index.html      The full site, with repository cards rendered into the markup
index.css       Styles, including the light and dark colour variables
config.json     Generator configuration: username, display name, sort order
blog/           One directory per write-up, each containing an index.html
dist/           Generator output, kept as the reference copy of a clean build
```

The site is served from the repository root, so `index.html` there is the live
page. `dist/` holds the same files as the generator produced them.

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

- Repository cards are baked into `index.html` at generation time, so stars,
  forks, and new repositories do not update until the page is regenerated or
  edited by hand.
- Several cards show no description or language because the underlying
  repositories have none set.
- Third-party assets load from CDNs, so the page depends on those staying
  available.

## Licence

Site content is mine. The underlying template is
[gitfolio](https://github.com/imfunniee/gitfolio) by
[@imfunniee](https://github.com/imfunniee), used under its own licence.
