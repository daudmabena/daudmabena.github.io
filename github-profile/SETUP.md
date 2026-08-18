# Publishing the profile README

Everything here takes one sitting. The result is a profile page whose images do
not break, because nothing on it depends on a third-party server staying online.

## 1. Create the profile repository

GitHub renders the README of a repository whose name matches your username, so
the repository must be named exactly `daudmabena`.

1. Create a new **public** repository named `daudmabena`.
2. GitHub will show a note confirming it is a special repository that appears on
   your profile. If that note is missing, the name does not match your username.
3. Do not initialise it with a template or licence; you only need the README.

## 2. Add the files

From this kit, copy into the new repository:

```
README.md                                  <- github-profile/README.md
.github/workflows/profile-cards.yml        <- github-profile/workflows/profile-cards.yml
.github/workflows/contribution-graph.yml   <- github-profile/workflows/contribution-graph.yml
```

Then work through `README.md` and resolve every `REPLACE:` marker. Each one is
either a value to fill in or a section to delete. Delete rather than fake:
an "Open Source" section with no real pull requests in it reads worse to a
reviewer than no such section.

## 3. Allow the workflows to commit

The workflows commit generated images back to the repository, which needs write
permission:

1. Open **Settings → Actions → General** in the `daudmabena` repository.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save.

No personal access token or repository secret is required. Both workflows use
the automatic `GITHUB_TOKEN`, which is scoped to this repository and expires when
the job finishes.

## 4. Generate the images once, before you publish

The README points at image files that do not exist until the workflows have run,
so run both now instead of waiting for the overnight schedule:

1. Go to the **Actions** tab.
2. Run **Update profile cards** via **Run workflow**. It commits
   `profile/stats.svg` and `profile/top-langs.svg`.
3. Run **Update contribution graph**. It creates the `output` branch holding
   `github-snake.svg` and `github-snake-dark.svg`.
4. Reload `https://github.com/daudmabena` and confirm all three images render.

After that both run daily on their own.

## 5. Finish the profile itself

The README is only part of what a visitor sees. In **Settings → Public profile**:

- Set your display name to **Daud Mabena**. It currently reads
  `DAUD ABASS MABENA`; all-capitals names read as a form field rather than a
  byline, and full capitals are how legal documents are written, not profiles.
- Set the bio (see `PROFILE_STRATEGY.md` for the wording).
- Set location to `Dar es Salaam, Tanzania`.
- Set the website to `https://daudmabena.github.io`.
- Leave the public email field empty unless the address is one you keep for
  public use. The README already gives people a way to reach you.
- Enable **Include private contributions on my profile**. It shows the volume of
  your private work as contribution counts without revealing repository names,
  which matters when most of your work is not public.

---

## Notes on the widgets used, and the ones left out

Requirement: reliable, currently supported, and no privacy or security exposure.
That rules out more of the popular profile-README ecosystem than most guides admit.

### Used

| Widget | How it is served | Why it is safe to rely on |
| --- | --- | --- |
| Statistics and top-languages cards | `stats-organization/github-readme-stats-action`, rendered in your own Actions run and committed as SVG | No runtime dependency on anyone's server. This is the deployment method the maintainers now recommend. |
| Contribution graph | `Platane/snk` (actively maintained, v3), rendered in your own Actions run | Same reasoning; reads only your public contribution calendar. |
| Two static text badges | `shields.io` | Static label images with no access to your account. Widely used and stable. |

### Deliberately left out

- **`github-readme-stats.vercel.app` image URLs.** The most copied snippet in
  profile READMEs, and the reason so many profiles show broken images. The
  shared public instance lost its sponsored hosting, is regularly rate limited,
  and has been paused. The workflow above renders the same cards without it.
- **`streak-stats.demolab.com` streak cards.** The public endpoints have
  returned errors for extended stretches, and the project itself recommends
  self-hosting. There is a workflow-based option if you want it, but a streak
  measures how many days in a row you pushed, not engineering quality, and it
  quietly encourages filler commits. Left out on both counts.
- **Trophy cards.** Award-styled graphics generated from ordinary public
  counters. They read as inflated, which is the opposite of what this profile
  is aiming for.
- **Profile view counters.** A visit tally is a vanity metric that reveals
  nothing about your work, and it hands a third-party service a log of who
  loads your profile.
- **WakaTime coding-time cards.** These require an editor plugin that
  continuously reports what files and projects you are working on to an external
  service. If you write code for employers or clients under confidentiality, do
  not install that, and note that hours logged is not evidence of skill.
- **Auto-generated "recent activity" feeds.** They fill the page with noise like
  starred repositories and comment stubs, and push your projects below the fold.

### If you ever add a widget yourself

Ask three questions first: is it still maintained, does the image render from
GitHub or from someone's free-tier server, and what account access does it
require? Anything that asks for a personal access token with `repo` scope so it
can display a larger number is not worth the credential.
