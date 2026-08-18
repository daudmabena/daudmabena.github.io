# Repository playbook

The profile README makes claims. Your repositories are where a reviewer checks
them. This is how to make each one hold up when someone actually opens it.

Apply the whole playbook to the four to six repositories you pin. Apply the first
two sections to everything else that stays public.

---

## 1. README files

Assume the README is the only file most visitors read. It should let someone
decide in thirty seconds whether the project is interesting, and let them run it
in ten minutes if it is.

Order matters, because most readers stop early:

1. **Project name and one-sentence summary.** What it does and who it is for. Not
   "A Laravel project" — "Fee collection and reconciliation system for a
   secondary school, built with Laravel and Oracle."
2. **Screenshot or short recording.** Immediately, before any prose. For anything
   with a user interface this is the single most persuasive element in the file.
3. **Status and links.** CI badge, licence, and a live demo link if one exists.
   Two or three badges, not a row of twelve.
4. **The problem.** Two or three sentences on what was wrong before this existed.
   This is what shows engineering judgement rather than tool familiarity, and it
   is the part almost every developer omits.
5. **Features.** Short bullets, capability-focused, honest about what is not done.
6. **Tech stack.** Versions included, so a reader knows what they need.
7. **Architecture.** A diagram plus a short paragraph. See section 4.
8. **Getting started.** Prerequisites, install, configure, run. See section 5.
9. **Testing.** How to run the tests, and what they cover.
10. **API documentation.** Or a link to it. See section 6.
11. **Project structure.** A short annotated tree of the directories that matter.
12. **Roadmap or known limitations.** Naming what is incomplete reads as
    confidence, not weakness. It is also honest.
13. **Licence and attribution.** Always, and mandatory for anything derived.

Use `templates/PROJECT_README_TEMPLATE.md` as the starting point.

Rules that matter more than they appear to:

- Write in plain English and run a spell check. Typos in a README invite doubt
  about care taken in the code.
- No "TODO: write README" left in a public repository.
- Never show real hostnames, database names, internal IP addresses, client names,
  or credentials, including in screenshots. Blur or substitute them.
- If the project came from client or employer work, either rebuild a generic
  version you own outright or do not publish it. Confidentiality mistakes are not
  recoverable, and a reviewer who suspects one will not raise it with you — they
  will simply move on.

## 2. Repository descriptions and topics

The description is the only text shown in search results, on your profile grid,
and in the pinned cards. Several of your repositories currently have none, which
makes them dead weight on the profile.

- One line, under about 100 characters, stating what the project does. Lead with a
  noun or verb, not "A repository for...".
- Add the website field for anything deployed. It renders as a clickable link on
  the repository card.
- Add five to ten topics: language, framework, domain, and project type — for
  example `laravel`, `php`, `oracle`, `rest-api`, `payments`, `dashboard`. Topics
  are how you get found by people browsing rather than searching.
- Name repositories in lowercase with hyphens, descriptively:
  `school-fees-management` rather than `sfm2` or `project-final`.

## 3. Screenshots

For anything with a user interface, screenshots are the highest-return effort in
this entire document.

- Commit them to `docs/screenshots/` and reference them with relative paths, so
  they survive independently of any image host.
- Capture at a consistent width (1440 pixels works well) with realistic but
  entirely fictional data. Never a production screen.
- Three to five views: the main dashboard, one key workflow, one form with
  validation visible, and a mobile or responsive view if relevant.
- Name them descriptively — `dashboard.png`, `invoice-create.png` — not
  `Screenshot 2026-08-18 at 10.32.14.png`.
- PNG for interfaces. Compress before committing; a README of 8 MB images is a
  performance problem on slow connections, which matters for your audience.
- For a workflow that is hard to convey statically, add one short GIF or MP4 under
  10 seconds. One, not a gallery.
- Write real alt text on every image.
- For Flutter, use device frames and show light and dark themes if you support both.

## 4. Architecture diagrams

A diagram is how you demonstrate architectural thinking in a form a reviewer can
absorb in seconds. Use **Mermaid**: GitHub renders it natively in Markdown, it
lives in version control as text, and it can be edited later without hunting for
the original design file. Examples in `templates/architecture-diagram.md`.

Worth drawing, in priority order:

- **System context.** Clients, your application, database, and external services.
  Draw this one for every non-trivial project.
- **Request flow.** A sequence diagram for the one interesting path — an
  authenticated API call, or a payment being initiated, confirmed, and reconciled.
  For your integration work, this is the diagram that carries the most weight.
- **Data model.** An entity-relationship diagram of the core tables. Show the
  central five or ten, not all sixty.
- **Deployment.** Nginx, PHP-FPM, application, database, queue worker, and where
  TLS terminates. This is where your server administration experience becomes
  visible instead of merely asserted.

Keep each diagram to one idea. Two clear diagrams beat one that tries to show
everything.

## 5. Installation instructions and environment configuration

The test is simple: clone the repository into an empty directory on a machine that
has never run the project, follow your own instructions literally, and change
nothing you have not written down. Most instructions fail this. Fix yours until it
passes.

Structure it as prerequisites with versions, then numbered commands, then how to
verify it worked.

For a Laravel project the sequence should be complete enough to copy and paste:

```bash
git clone https://github.com/daudmabena/<repository>.git
cd <repository>
composer install
cp .env.example .env
php artisan key:generate
# configure database credentials in .env, then:
php artisan migrate --seed
npm install
npm run build
php artisan serve
```

End with what success looks like: "Open http://localhost:8000 and sign in with
`admin@example.test` / `password` from the seeder."

### Environment configuration

- Commit a complete `.env.example` listing **every** variable the application
  reads, with safe placeholder values and a comment on each non-obvious one.
  Missing variables are the most common reason a stranger fails to run a project.
- `.env` in `.gitignore`, always. Verify it is not already tracked:
  `git ls-files | grep -i env`.
- Placeholders must be obviously fake — `DB_PASSWORD=changeme`, not a real
  password with characters swapped.
- Document which variables are required versus optional, and note anything that
  needs an external account, such as sandbox payment credentials.
- **If a real secret has ever been committed, rotate it now.** Removing it in a
  later commit does not remove it from history, and public repositories are
  scanned continuously by automated tooling. Enable secret scanning and push
  protection in repository settings.
- Never commit database dumps containing real data. For Oracle work, share a
  schema creation script instead of an export.

## 6. API documentation

This is where you can visibly outperform, because it is the part most developers
skip — and because your profile leads with API design.

- Write an **OpenAPI** specification and commit it as `openapi.yaml`. It is the
  format reviewers and integrators expect, and it can generate a client. A
  Postman collection exported to `docs/postman_collection.json` is an acceptable
  alternative, and a good supplement.
- Document, once, at the top: base URL, authentication scheme, how to obtain a
  token, pagination, and the standard error envelope. Then per endpoint: method
  and path, parameters with types and whether required, an example request, and
  example responses for both success and the common failure.
- Show error responses, not just the happy path. An API documented only in its
  success case tells a reviewer you have not thought about failure — the opposite
  of the impression you want for financial workflows.
- State your versioning approach, even if it is only "`/api/v1`, breaking changes
  go to v2".
- Rendered documentation, published with GitHub Pages, is a strong touch. Keep the
  specification as the source of truth so it cannot drift.
- Use fictional identifiers in every example. No real account numbers, customer
  names, or transaction references.

## 7. Tests

Tests are read as a proxy for whether you can be trusted with a system other
people depend on. You do not need high coverage; you need tests that clearly test
something that matters.

- Cover the core logic first: the calculation, the validation rules, the state
  transitions. For payment and financial code, cover the edge cases explicitly —
  zero and negative amounts, rounding, duplicate submission, partial failure.
- Laravel: Pest or PHPUnit, with feature tests over the important endpoints. A
  test asserting a request without authentication returns 401, and that an invalid
  payload returns 422 with the documented error shape, communicates a great deal.
- React: Vitest with React Testing Library for a few component and hook tests.
- Flutter: `flutter test` for widget tests on the key screens.
- Name tests as sentences describing behaviour:
  `test_invoice_total_excludes_cancelled_items`.
- Tests must pass on a clean clone with documented setup. A failing test suite is
  worse than none, because it suggests you did not run it.
- Skip coverage badges unless the number is genuinely good; a badge reading 11%
  draws attention to exactly what you would rather it did not.

## 8. CI/CD

A green check on the commit list is a small, immediate credibility signal, and it
proves the project builds outside your machine.

Start minimal — install dependencies, run the linter, run the tests, on push and
pull request. Templates for both stacks are in this directory:

- `templates/laravel-ci.yml`
- `templates/react-vite-ci.yml`

Then, in rough order of value:

- Add the status badge to the README, pointing at the workflow.
- Add code style enforcement: Laravel Pint for PHP, ESLint and Prettier for
  TypeScript. Run them in CI so style stops being a discussion.
- Test against the PHP versions you claim to support.
- For a deployed frontend, deploy from CI on merge to `main`. A live link that is
  always current is worth more than any badge.
- Enable Dependabot for security updates. Merged dependency pull requests are
  genuine evidence of maintenance.

Keep secrets in GitHub Actions secrets, never in the workflow file. Do not put
production deployment credentials in a public repository's CI at all.

## 9. Commit history

Reviewers do read commit history, and it is the clearest available evidence of how
you work day to day.

- Write messages in the imperative mood, explaining the change:
  `Add invoice reconciliation report` rather than `update`, `fix`, `changes`, or
  `asdf`. Several of your repositories currently have messages of that second
  kind, including `Editing the README to try out git add/commit`.
- Consider Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`,
  `chore:`). Cheap to adopt, immediately legible, and it is what teams expect.
- One logical change per commit. Not one commit per day of work, and not
  "Start new Portfolio" three times in a row.
- Where a change is not self-explanatory, use the commit body to say why, not what.
  The diff already shows what.
- Never commit `vendor/`, `node_modules/`, build output, `.env`, or IDE
  directories. Check your `.gitignore` before the first push.
- Make sure your commit email matches your GitHub account, or the contributions do
  not appear on your profile at all. Verify with `git log --format='%ae' | sort -u`.
- Enable commit signing so commits show as "Verified". A small detail that
  security-conscious reviewers notice.
- Do not rewrite the history of old public repositories to look tidier. Going
  forward is enough; a manufactured history is both detectable and pointless.

## 10. Issues and pull requests

On your own repositories, using issues and pull requests instead of committing
straight to `main` demonstrates process — which is a large part of what
distinguishes a professional developer from a capable hobbyist.

- Work on branches and merge via pull requests, even alone. The pull request
  becomes the written record of what changed and why.
- Write real pull request descriptions: the problem, the approach, how you tested
  it, and screenshots for user-facing changes. Use
  `templates/pull_request_template.md`.
- Track work as issues rather than in a text file, and close them from the pull
  request with `Closes #12`. This is what makes a repository look maintained.
- Label meaningfully — `bug`, `enhancement`, `documentation`, `good first issue` —
  and keep the set small.
- Add `CONTRIBUTING.md` to any repository you would accept contributions to, and
  a `LICENSE` to every public repository. Without a licence, nobody can legally
  reuse your code, which undercuts the point of publishing it.
- Respond to issues opened by strangers, even to say you will not act on them. An
  unanswered issue from two years ago is visible to everyone.
- Do not manufacture issues and pull requests against yourself for appearances.
  It is obvious, and it is the sort of thing that loses the benefit of the doubt
  elsewhere.

---

## Priority order

If you only do part of this, do it in this order:

1. `.env` and secrets out of every public repository, and any exposed credential
   rotated. Security first, and it is the only item here that is urgent.
2. Descriptions and topics on everything public. An hour's work, immediately
   visible on your profile.
3. One excellent README, with screenshots, on your strongest project.
4. Working installation instructions on that project, verified from a clean clone.
5. CI running tests on it, with the badge in the README.
6. Architecture diagram and API documentation on the API project.
7. Everything else.
