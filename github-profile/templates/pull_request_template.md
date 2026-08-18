<!--
  Install at .github/pull_request_template.md in a project repository.
  GitHub then pre-fills every new pull request with this.

  Worth doing even on solo projects: the pull request becomes the written record
  of what changed and why, and a reviewer reading your repository sees a
  deliberate process rather than a stream of commits straight to main.
-->

## What this changes

<!-- One or two sentences. What does this do, and why now? -->

## Related issue

<!-- Closes #12 — the keyword closes the issue automatically on merge. -->

## Approach

<!-- Only for non-obvious changes: what you chose to do, and what you rejected.
     This is the part your future self will want. -->

## How this was tested

<!-- Commands run, cases covered, and anything checked by hand. -->

- [ ] Automated tests added or updated
- [ ] Test suite passes locally
- [ ] Verified manually

## Screenshots

<!-- Required for any user-facing change. Before and after, if it is a change to
     something that already existed. Delete the section otherwise. -->

## Checklist

- [ ] No credentials, real data, or `.env` values in the diff
- [ ] Documentation updated if behaviour or setup changed
- [ ] `.env.example` updated if a new variable was introduced
- [ ] Database migrations are reversible
- [ ] No debugging leftovers (`dd`, `console.log`, commented-out code)
