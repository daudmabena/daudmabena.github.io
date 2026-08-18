# GitHub profile kit

Everything needed to turn `github.com/daudmabena` into a profile that reads as the
work of a professional software developer, plus the plan for making the
repositories behind it hold up when someone opens them.

## Files

| File | What it is |
| --- | --- |
| [`README.md`](README.md) | The profile README, ready to copy into a repository named `daudmabena`. Placeholders are marked `REPLACE:`. |
| [`SETUP.md`](SETUP.md) | How to publish it: create the repository, install the workflows, generate the statistics images, finish the account settings. Also documents which widget services were used and which were rejected, and why. |
| [`PROFILE_STRATEGY.md`](PROFILE_STRATEGY.md) | Why each README section is there, username and display-name strategy, bio wording, profile photograph and banner concepts, which repositories to pin and in what order, the full checklist, and a thirty-day plan. |
| [`REPOSITORY_PLAYBOOK.md`](REPOSITORY_PLAYBOOK.md) | How to bring repositories up to standard: READMEs, descriptions, screenshots, diagrams, installation, API documentation, environment configuration, tests, CI/CD, commit history, issues and pull requests. |
| [`workflows/profile-cards.yml`](workflows/profile-cards.yml) | Generates the statistics and top-languages cards inside your own repository, so they do not break when a shared public service goes down. |
| [`workflows/contribution-graph.yml`](workflows/contribution-graph.yml) | Renders the contribution calendar as an animated SVG, published to a separate branch to keep the main history clean. |
| [`templates/`](templates) | Project README template, Mermaid architecture diagram patterns, CI workflows for Laravel and React, and a pull request template. |

## Order to work through it

1. `SETUP.md` — publish the profile. One sitting.
2. `PROFILE_STRATEGY.md`, Part 4 — decide what to pin, and what to archive.
3. `REPOSITORY_PLAYBOOK.md` — bring the strongest project up to standard, then the next.
4. `PROFILE_STRATEGY.md`, Part 6 — the thirty-day plan, if you want a schedule.

## Two things worth knowing before you start

**The README is the smaller half of the job.** It states what you do; your
repositories are where a reviewer checks whether it is true. Your public
repositories are currently mostly small jQuery, WordPress, and mysqli utilities,
which do not match a profile describing Laravel, React, Flutter, Oracle, and
payment integrations. Closing that gap matters more than any wording choice, and
`PROFILE_STRATEGY.md` Part 4 sets out how.

**Nothing here invents anything on your behalf.** Every project, statistic,
certification, and contribution is left as a marked placeholder for you to fill
in or delete. That is deliberate: a profile is only useful if it survives an
interview, and the fastest way to lose a technical reader is a claim that does
not hold up under one question.
