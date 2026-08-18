# Profile strategy

Reference material for the README in this directory: why it is built the way it
is, and the decisions that sit outside the README file itself.

---

## Part 1 — Why each section is there

A profile README is read in roughly fifteen seconds by someone deciding whether
to keep reading. Every section below has to earn its place in that window.

### Header: name, one-line role, contact row

The first screen answers three questions a recruiter or client asks immediately:
what do you do, what do you do it with, and can I reach you. Naming the three
technologies you actually work in (Laravel, React, Flutter) makes the profile
findable and filterable by someone scanning many candidates. The contact row sits
above the fold because a profile that impresses someone but gives them no way to
follow up has wasted the impression.

Two static badges, not twenty. A wall of technology badges is the clearest signal
that a profile was assembled from a template, and it flattens everything into one
undifferentiated list where Tailwind looks as significant as Oracle.

### About Me

Three short paragraphs, written in prose, doing what a bullet list cannot: state
what kind of problem you work on rather than which keywords you know. The
sentence about integrations "between systems that were not originally designed to
talk to each other" describes work that is genuinely difficult and that most
junior developers have never done. That distinction is the point of the section.

The closing paragraph on maintainability signals seniority without claiming it.
Caring about data models, documented APIs, and predictable deployments is what
separates someone who ships features from someone trusted with a system other
people depend on.

### What I Build

Recruiters and technical leads search for domain experience as much as for
languages, and "financial and payment systems" is a domain filter that carries
real weight: it implies you have handled correctness under money constraints,
reconciliation, and failure paths that must not silently drop transactions. The
table format matters because the second column converts each label into something
checkable. "Enterprise applications" alone is a claim anyone can type; "role-based
access, audit trails, and reporting" tells a reader what you have actually built.

### Technology Stack

Grouped by role in a system rather than as one long list, so a reader can
immediately see you are not a single-layer developer: you cover frontend,
backend, mobile, database, and infrastructure. That breadth, laid out clearly, is
what makes you plausible for end-to-end ownership of a system.

Written as plain text rather than badge images for three reasons. It stays
readable when images are blocked or a badge service goes down, it does not turn
a technical summary into decoration, and it lets you list things that have no
badge, like "relational database design" or "server administration".

The section is also honest about its own limits: the note under the statistics
cards points out that language totals measure bytes of code, not skill. Saying so
before a reviewer thinks it makes the rest of the profile more credible.

### Engineering Strengths

The most important section for a technical reader, because it is the only one
that explains *how* you work rather than *what* you know. Each line names a
specific practice — request validation, indexing and query tuning, handling
partial failures and retries — that a reviewer can probe in an interview. This is
deliberate. Claims you can defend under questioning are the kind worth making,
and it is why there is no "expert" or "10x" language anywhere: a specific
verifiable statement is always stronger than a superlative.

### Featured Projects

The single highest-value section, and the one that carries the profile. Everything
above it is a claim; this is the evidence. A reviewer who is interested will click
exactly one thing, so the table is limited to four to six entries with a stated
problem, the stack, and a live link where one exists. Pinned repositories with
strong READMEs are what convert a profile view into a conversation.

### Open Source

Contributions to other people's codebases demonstrate something your own
repositories cannot: that you can read unfamiliar code, follow a project's
conventions, take review feedback, and get a change merged past a maintainer who
has no reason to be generous. That is a direct proxy for how you will behave on a
team. The section is written to be deleted if it is empty, because a placeholder
section here reads as an unfulfilled intention.

### GitHub Statistics and Contribution Activity

These sections meet an expectation — a bare profile can look inactive — while
being carefully scoped. Both images are generated inside your own repository by
GitHub Actions rather than loaded from a shared free-tier server, which is what
keeps them from becoming broken placeholders later. `SETUP.md` covers that
reasoning and lists the popular widgets left out on reliability and privacy
grounds.

The note stating that much of your work is private and self-hosted does real work
for you. A sparse graph invites the wrong conclusion; one sentence reframes it
accurately and honestly.

### Education and Certifications

Included conditionally, because relevance decides its value. A degree or a
meaningful certification (Oracle, AWS, Linux) adds credibility, especially early
in a career and especially with non-technical screeners. A list of short online
course badges dilutes the page. Two real entries beat ten weak ones.

### Contact

Gives a professional route in — email, LinkedIn, portfolio — and deliberately
omits phone number, physical address, and personal identifiers. A GitHub profile
is permanently public and continuously scraped. Nothing in that omitted list
helps anyone evaluate your engineering, and all of it is impossible to withdraw
once indexed. Share it privately when a conversation becomes real.

---

## Part 2 — Username and naming

### Your username

**Keep `daudmabena`.** It already meets every criterion that matters: it is your
real name, lowercase, no digits, no underscores or hyphens, no fashion reference
that will date, and it is unambiguous to type from memory after someone hears it.
It is also consistent with `daudmabena.github.io`, so your portfolio URL and your
profile URL match — which is worth more than any cosmetic gain from renaming.

Renaming is a bad trade here in any case: GitHub frees your old username for
anyone to claim, links in old commits, CVs, and job applications break, and
`daudmabena.github.io` would stop resolving. Do not do it.

For reference, these are the properties worth optimising for, all of which you
already have: recognisably your name, short, all lowercase, no numbers, no
year-of-birth, no `dev`/`coder`/`ninja` suffix, and identical or near-identical
across GitHub, LinkedIn, and your domain.

### Your display name

Change it from `DAUD ABASS MABENA` to **Daud Mabena**. Full capitals read as a
filled-in form field rather than a name, and dropping the middle name matches how
you will be addressed in email and how your LinkedIn profile should read. Use the
same form everywhere, so the three profiles are obviously the same person.

### One detail worth fixing

Your organisation displays as `DYCODEDESINGS`, which appears to be a
transposition of `DESIGNS`. Similarly, the repository `Woordpress-Snippets`
carries a visible misspelling of WordPress. These are small, but a reviewer
assessing attention to detail sees them at the same moment they are deciding
whether your code is careful. Fix the organisation display name, and rename or
archive the repository.

---

## Part 3 — Bio, avatar, and banner

### Bio

GitHub allows 160 characters. It appears beside your avatar, in search results,
and next to every comment you leave on other projects, so it needs to work
standing alone. Lead with the role, name the domain, then the stack.

Recommended:

> Software developer building enterprise systems, APIs, and integrations with Laravel, React, and Flutter.

Alternatives, depending on the work you want to attract:

> Backend-focused software developer. Laravel and PHP, React and TypeScript, Flutter. Enterprise systems and payment integrations.

> Software developer in Dar es Salaam. I build enterprise web systems, REST APIs, and financial system integrations.

Leave out "passionate", "aspiring", "self-taught", "coding enthusiast", and
quotations. Do not put your location in the bio; there is a separate location
field for it.

### Profile picture

The avatar appears at roughly 40 pixels next to comments, so it has to survive
being small. What works:

- A recent head-and-shoulders photograph, face filling most of the frame, looking
  at the camera, with a relaxed but neutral expression.
- Even, soft light from the front. A window at midday, facing you, is enough.
- A plain, uncluttered background a clear shade away from your skin tone and
  clothing. A wall works.
- Business-casual clothing in a solid colour, no busy patterns.
- Square crop, at least 500×500, exported as PNG or high-quality JPEG.

What to avoid: group photographs, sunglasses, heavy filters, a logo or cartoon
avatar in place of a face, a screenshot of code, and the default identicon. The
default is the single most common reason a profile reads as abandoned.

### Banner concept

GitHub does not have a profile banner field, so a banner is an image at the top of
the profile README. It is optional — the README works without one, and a poor
banner is worse than none. If you want one:

- **Dimensions:** 1280×320 (a 4:1 strip), PNG. It renders well at full width and
  does not push your content off the first screen.
- **Layout:** name at left in a clean sans-serif (Inter, Poppins, or Source Sans
  Pro), the line "Software Developer — Laravel · React · Flutter" beneath it in a
  lighter weight and smaller size, and generous empty space to the right.
- **Colour:** one deep, low-saturation background — slate, deep navy, or near
  black — with off-white text and a single accent colour used once. Two colours
  plus a neutral, no gradients that fight with the text.
- **Optional detail:** a faint geometric motif at low opacity on the right side,
  suggesting structure rather than illustrating anything. Keep it subtle enough
  that text remains the loudest element.
- **Do not include:** a grid of technology logos, stock photographs of code on a
  monitor, "Welcome to my profile", handwriting fonts, or your email address as
  an image.
- **Accessibility:** keep text contrast high, and give the image real alt text
  (`alt="Daud Mabena — Software Developer"`), not `alt="banner"`.

Store it in the profile repository at `assets/banner.png` and uncomment the block
at the top of `README.md`. Verify it in both GitHub light and dark themes; a
transparent PNG that looks correct in one will disappear in the other, so use a
solid background.

---

## Part 4 — Which repositories to feature and pin

GitHub allows six pinned repositories, shown in order, immediately under your
README. They are the most-clicked thing on the page.

### What makes a repository worth pinning

Pin for evidence of engineering judgement, not for volume:

1. **It solves a stated problem.** The README opens with what it does and for whom.
2. **It reflects the stack you advertise.** Laravel, React and TypeScript,
   Flutter, Oracle. A profile claiming Laravel and React that pins only jQuery
   snippets creates a gap a reviewer will notice.
3. **It is substantial enough to read.** A reviewer wants to see how you
   structure a project — layers, naming, error handling, tests — which a
   single-file snippet cannot show.
4. **It is yours.** Original work, or clearly attributed if derived.
5. **It is presentable.** README, screenshots, setup instructions that work.
6. **It is finished enough to run.** A working small project beats an ambitious
   abandoned one.

### Your current position, honestly

Taken from the GitHub API rather than from memory: **344 public repositories, of
which 292 are forks and 44 are your own.** Nothing is archived.

**The forks are being ignored, not cleaned up.** That is a deliberate decision and
a reasonable one — archiving 292 repositories by hand is a poor use of time, and
the places that matter already leave them out:

- The portfolio site excludes them (`include_forks: false` in
  `tools/site.config.json`).
- The most-used-languages card excludes them: it only ever reads repositories you
  own and have not forked, so your language totals are unaffected.
- Commits inside a fork do not count as contributions, so the statistics card and
  contribution graph are unaffected too.

The one place they stay visible is the Repositories tab on your profile, which has
no setting to hide forks. Accept that. Nobody forms their impression of you from
that tab — they read the README and click the pinned repositories, and forks
appear in neither. If it ever starts to bother you, archiving is the only remedy,
and it can be done gradually.

**The more useful correction is that your own recent work is better than your old
public repositories suggest.** Alongside the 2013–2017 material (jQuery table
helpers, WordPress themes, mysqli wrappers, PHP form validation) there is a
substantial run of recent, relevant projects that the portfolio had never shown:

| Repository | Language | Last pushed |
| --- | --- | --- |
| `bismuth-cms` | TypeScript | 2026 |
| `Vendite-Maestria` | PHP | 2026 |
| `task-manager` | TypeScript | 2026 |
| `curl_post` | TypeScript | 2026 |
| `my_flask_api` | Python | 2026 |
| `legal-content-writer` | JavaScript | 2026 |
| `olas-admin` | TypeScript | 2024 |
| `noasis-training` | TypeScript | 2022 |
| `yii2-bs4-basic`, `yii2-bs4-advanced` | PHP | 2021 |

This changes the priority. The gap between what your profile claims and what your
repositories show is narrower than the old public list implied — but these
repositories are undocumented, which makes them invisible as evidence. **15 of your
44 own repositories have no description at all, and 43 of 44 have no topics.** A
reviewer opening `bismuth-cms` today finds no README, no description, and no
explanation of what it is.

So the highest-value work is not building something new. It is documenting two or
three of the projects you have already written, using
`REPOSITORY_PLAYBOOK.md`. That converts existing work into evidence, which is far
cheaper than starting again.

Two things still worth handling directly:

- **Work that is not yours.** `Mysqli-wrapper` (its own description credits another
  author), `summernote_wysiwyg`, `Public-social-Api-php`, `mimic-tool-box`,
  `Hueman-Child-Theme`, and `lukaszfiszer.github.io` (another developer's personal
  site) are not forks, so GitHub shows no upstream link and they read as your own.
  Either state the origin and licence at the top of each README, or archive them.
  Nothing damages technical credibility faster than appearing to present someone
  else's library as your own. These are already left off the portfolio site.
- **Repositories that are empty or scaffolds.** `lms`, `fadhatech`, `application`,
  `example-app`, `dudee`, and `AwesomeProject` show no primary language or are
  untouched framework scaffolds. They are excluded from the site; leaving them
  public is harmless, but do not pin them.

`FADHATECHNOLOGY/comas` is no longer publicly available, so the card that used to
link to it has been dropped from the site.

Archiving, where you do use it, is not deletion. An archived repository stays
available but is marked read-only, which is what you want for old work you do not
wish to hide but do not wish to be judged on.

### Pinning order

Order deliberately: strongest first, and lead with the stack you want to be hired
for. Aim for this shape.

1. **Your most complete Laravel + database system.** The flagship. Ideally an
   enterprise-style application showing authentication, roles, a non-trivial
   schema, and reporting. This is the one that has to be genuinely good.
2. **A REST API project with real documentation.** Because API design is central
   to how you describe yourself, and documentation is the part most developers
   skip, this is where you visibly outperform. Include the OpenAPI specification
   or a Postman collection.
3. **A React + TypeScript frontend.** Proves the frontend claim independently,
   with Vite, Tailwind, and Zustand in evidence. A deployed link matters most here
   — reviewers will click it.
4. **A Flutter application.** Covers mobile, and widens the roles you match.
   Screenshots of the running app are essential.
5. **An integration or payment-workflow project.** Your genuine differentiator.
   Build a self-contained demonstration against a payment provider's sandbox, or a
   mock provider — never anything touching real credentials or employer systems.
   Document the failure handling and retry behaviour; that is the interesting part.
6. **`daudmabena.github.io`, or a curated utilities repository.** A portfolio site
   is a reasonable sixth. Put the consolidated utilities repository here instead
   once it exists.

Until repositories 1 to 5 exist, pin the best of what you have rather than filling
all six slots. **Four strong pins are better than six that include two weak ones**,
because a reviewer's impression is set by the weakest thing they open.

### Candidates you already have

Rather than starting from nothing, these are the existing repositories closest to
the shape above. Each needs a description, topics, and a README before it is worth
pinning — that is the work, not the code.

| Slot | Best existing candidate | What it needs |
| --- | --- | --- |
| Laravel or PHP flagship | `Vendite-Maestria` (PHP, 2026) | Confirm it is substantial, then document it fully |
| REST API with documentation | `my_flask_api` (Python) or `curl_post` (TypeScript) | An OpenAPI specification, plus documented errors. Python is off your advertised stack, so prefer a PHP or TypeScript API if you have one |
| React and TypeScript frontend | `bismuth-cms`, `olas-admin`, or `task-manager` (all TypeScript) | A description, a README, screenshots, and a deployed link |
| Yii2 example | `yii2-bs4-basic` or `yii2-bs4-advanced` | Check first whether these are your own work or copies of the standard Yii2 application templates. If they are the stock templates, do not pin them |
| Flutter application | none public | The one genuine gap. Nothing in your public repositories is Dart or Flutter, so the mobile claim in the README currently has no public evidence behind it |
| Integration or payment workflow | none public | Also unevidenced publicly. This is your strongest differentiator, so a small sandbox demonstration is worth more here than anywhere else |

Two of the six categories have no public evidence at all: **Flutter and payment
integrations**. Those are precisely the two things that most distinguish your
README from an average one, so they are the highest-return things to build. Keep
the claims in the README — they are true of your professional work — but be aware
a reviewer cannot currently verify them, and expect to be asked in an interview.

Anything you can build from scratch works here — you do not need employer code,
and you should not use it. Rebuilding a system you understand well, at smaller
scale, with clean architecture and documentation, is more impressive than a
partial extract of a large private codebase, and it carries no confidentiality risk.

---

## Part 5 — Profile improvement checklist

Repository-level work is in `REPOSITORY_PLAYBOOK.md`.

### Account settings

- [ ] Display name set to `Daud Mabena` (currently `DAUD ABASS MABENA`)
- [ ] Profile photograph meeting the criteria above
- [ ] Bio replaced. The current one reads "Software Developer who love to create
      things that uplift the community, happy to lean new thing daily", which
      contains three errors — "who love", "lean" for learn, and "new thing". It
      appears beside every comment you leave on other projects, so it is worth
      fixing before anything else on this list.
- [ ] Location set to `Dar es Salaam, Tanzania`
- [ ] Website field pointed at `https://daudmabena.github.io` (currently
      `dev.page/daud`), now that the portfolio is current
- [ ] `@FADHATECHNOLOGY` company field checked for the trailing space
- [ ] LinkedIn added to profile links, with matching name and headline
- [ ] Public email either a dedicated professional address or left blank
- [ ] "Include private contributions on my profile" enabled
- [ ] Two-factor authentication enabled
- [ ] Commit email consistent across machines, so contributions are attributed
- [ ] Vigilant mode on and commit signing configured, so commits show "Verified"
- [ ] `DYCODEDESINGS` organisation display name spelling corrected

### Profile README

- [ ] `daudmabena/daudmabena` repository created, public
- [ ] README added and every `REPLACE:` marker resolved or deleted
- [ ] Both workflows installed and run once, all images rendering
- [ ] Workflow permissions set to read and write
- [ ] Featured Projects table filled with real repositories
- [ ] Open Source section either populated with real pull requests or removed
- [ ] Education section either populated or removed
- [ ] Rendering checked in light and dark themes, and on a phone
- [ ] Every link clicked and confirmed working
- [ ] Read once for exaggeration: no superlatives, no invented numbers

### Repository presentation

- [x] Forks ignored rather than archived — already excluded from the portfolio
      site and from the language card, and they cannot be hidden from the
      Repositories tab, so no action is being taken
- [ ] Descriptions added to your own repositories: 15 of 44 have none, including
      recent work like `bismuth-cms`, `olas-admin`, and `curl_post`
- [ ] Topics added: 43 of 44 have none, so none of them surface in browsing
- [ ] Work that is not yours attributed in its README or archived
      (`Mysqli-wrapper`, `summernote_wysiwyg`, `Public-social-Api-php`,
      `mimic-tool-box`, `Hueman-Child-Theme`, `lukaszfiszer.github.io`)
- [ ] Two or three recent projects documented to the standard in
      `REPOSITORY_PLAYBOOK.md` — the highest-value item on this list
- [ ] Four to six repositories pinned, strongest first
- [ ] Each pinned repository has a README with screenshots and working setup steps
- [ ] No credentials, `.env` files, dumps, or client data in any public history

### Ongoing

- [ ] Contributions genuinely spread across weeks, not manufactured streaks
- [ ] Issues and pull requests used on your own projects, so the history shows process
- [ ] At least one external contribution in progress
- [ ] Profile reviewed quarterly against the stack you currently work in

---

## Part 6 — Thirty-day plan

Roughly an hour on weekdays and a longer block at weekends. The order is
deliberate: presentation first because it is quick, then the substantive work of
building something worth showing.

### Week 1 — Publish the profile and clean up

- **Day 1.** Create `daudmabena/daudmabena`. Add the README. Resolve the
  `REPLACE:` markers you can answer immediately, and delete the Open Source and
  Education sections for now.
- **Day 2.** Install both workflows, set workflow permissions, run them, confirm
  the images render in light and dark themes.
- **Day 3.** Account settings: display name, photograph, bio, location, website,
  private-contribution visibility, two-factor authentication.
- **Day 4.** Write a one-line description for each of your own repositories that
  has none — 15 of them, including `bismuth-cms`, `olas-admin`, and `curl_post`.
  This is the fastest visible improvement available, and it needs no code. Skip
  the forks entirely.
- **Day 5.** Add five to ten topics to the repositories worth keeping, so they
  surface when people browse. Attribute the repositories that hold other people's
  code. Correct the organisation name spelling.
- **Weekend.** Open your three most recent projects and decide, honestly, which
  one is closest to being presentable. That is the subject of week 2.

### Week 2 — Make one project genuinely good

Depth on one repository beats shallow edits across five. Start with the project
you chose at the weekend — most likely `Vendite-Maestria` or `bismuth-cms` — rather
than starting something new. Documenting code you have already written is much
cheaper than writing more.

- **Day 8.** Write the README properly, using the template in
  `templates/PROJECT_README_TEMPLATE.md`.
- **Day 9.** Screenshots of the running application, committed under `docs/`.
- **Day 10.** An architecture diagram, as Mermaid so it stays editable in the
  repository. Examples in `templates/architecture-diagram.md`.
- **Day 11.** Setup instructions, followed literally on a clean clone. Fix every
  step that fails. Add `.env.example` with no real values.
- **Day 12.** Tests for the core logic. A handful of meaningful tests beats a
  coverage badge.
- **Weekend.** CI workflow from `templates/`. Get the badge green, then pin this
  repository first.

### Week 3 — API documentation and the integration piece

- **Day 15.** Choose or build the REST API project. Settle the resource design.
- **Day 16.** Write the OpenAPI specification, or export a Postman collection,
  and commit it.
- **Day 17.** Document authentication and the error format, with request and
  response examples for every endpoint.
- **Day 18.** Start the integration demonstration: a payment or third-party
  workflow against a sandbox or a mock provider. No real credentials, ever.
- **Day 19.** Implement the failure paths — validation, timeouts, retries,
  idempotency — and document them. This is the part that distinguishes you.
- **Weekend.** README, diagram, and CI for both repositories. Pin them second and
  fifth.

### Week 4 — Frontend, mobile, and open source

- **Day 22.** React and TypeScript project: finish it, then deploy it to GitHub
  Pages, Netlify, or Vercel and link it from the README.
- **Day 23.** Flutter application: screenshots of the running app, plus build
  instructions.
- **Day 24.** Find a first external contribution. Realistic starting points:
  documentation gaps in Laravel packages you already use, `good first issue`
  labels in the Laravel and PHP ecosystem, or a bug you have personally hit in a
  dependency. Read the contributing guide before writing anything.
- **Day 25.** Submit it. Small and correct, with a clear description of the
  problem and the fix. Respond to review promptly.
- **Day 26.** Fill in the Featured Projects table with what now exists. Restore
  the Open Source section once the pull request is open, and the Education section
  if it applies.
- **Weekend.** Final pass: set the pin order, click every link, reread for
  exaggeration, view the profile on a phone. Ask someone whose judgement you
  trust what they think you do after fifteen seconds on the page. If their answer
  does not match "backend and integrations developer", the top of the README needs
  another edit.

### After the first month

The profile is done; the repositories never are. Maintaining it takes far less
than building it:

- One meaningful commit to a public project most weeks, real work rather than
  streak filler.
- One external contribution a month.
- Revisit the pinned set each quarter, and replace the weakest pin whenever
  something better exists.
- Reread the top of the README whenever your work changes, so what it claims
  stays true.
