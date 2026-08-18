# Images

## avatar.jpg — the profile photo

**Drop your headshot in this directory as `avatar.jpg`.** Nothing else is needed:
`index.html` already points here, and falls back to your GitHub avatar until the
file exists, so the page is never broken either way.

Requirements:

- Square, at least 460 × 460 pixels (larger is fine; it is scaled down)
- JPEG, saved at around 80% quality
- Under about 150 KB — it is the only image on the page, so keep it light

Once it is committed, also switch these two lines in `index.html` from the GitHub
URL to the local file, since neither can use the JavaScript fallback:

```html
<meta property="og:image" content="https://daudmabena.github.io/assets/img/avatar.jpg" />
<link rel="icon" href="assets/img/avatar.jpg" type="image/jpeg" />
```

`og:image` must stay an absolute URL — social networks fetch it from outside the
site, so a relative path will not resolve for them.

## Do this first: update the GitHub profile picture

Higher leverage than the file above, and it takes a minute.

Upload the same photo at **Settings → Public profile → Profile picture** on
GitHub. That single change updates your avatar on the profile page, next to every
comment and pull request you have ever written, on the profile README, and on this
site — because the fallback here reads `https://github.com/daudmabena.png`.

Your current GitHub avatar is a casual photograph taken in a car. The studio
headshot is a significant improvement and meets every criterion in
`github-profile/PROFILE_STRATEGY.md`: head and shoulders, facing the camera, even
front lighting, a plain uncluttered background, business attire, and a neutral
expression that still reads as approachable. It also stays legible at the 40-pixel
size GitHub renders beside comments, which is where most people will actually see
it.

Use the same photograph on LinkedIn. Consistency across profiles is what makes
them recognisably one person.
