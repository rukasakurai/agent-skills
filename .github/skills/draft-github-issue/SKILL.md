---
name: draft-github-issue
description: 'Turn a discussion, bug report, or code analysis into a lean, problem-focused GitHub issue and file it with the gh CLI. Use when you need to capture a problem as a well-scoped issue that separates the problem from the solution, keeps scope tight, leaves implementation freedom to the assignee, and avoids creating duplicates.'
argument-hint: 'Describe the problem or paste the discussion to turn into an issue'
---

# Draft GitHub Issue

Turn a discussion, bug report, or code analysis into a lean, problem-focused GitHub
issue and file it with the `gh` CLI.

## When to Use

- You have a discussion, investigation, or code analysis that should become a tracked issue.
- You want an issue that clearly states the problem without over-prescribing the solution.
- You need to file the issue reliably without creating duplicates.

## Principles

1. **Separate the problem from the solution.** Lead with the problem and its impact.
   Capture desired behavior as outcomes, not implementation steps.
2. **Keep it lean.** Include only what the assignee needs to understand and act.
   Cut background that does not change the work.
3. **Leave implementation freedom.** State constraints and acceptance criteria, then
   explicitly let the assignee choose how to satisfy them.
4. **State constraints explicitly.** Call out hard requirements (conventions, security,
   compatibility) so freedom is bounded, not unlimited.

## Issue Template

Draft the issue body using this structure. Omit any section that adds no value.

```markdown
## Problem

<What is wrong or missing, and why it matters. Observable symptoms, not fixes.>

## Desired behavior

<The outcome once this is resolved, described as behavior — not implementation.>

- <outcome / acceptance criterion>
- <outcome / acceptance criterion>

## Constraints

<Hard requirements the solution must respect, e.g. conventions, security, compatibility.>

The assignee is free to decide how to satisfy the desired behavior within these constraints.
```

## Procedure

1. **Gather the source material.** Read the discussion, bug report, or analysis.
   Identify the single core problem; split unrelated problems into separate issues.
2. **Draft the title.** One line, problem-focused, specific (e.g.
   "Add draft-github-issue skill for cross-repo/computer reuse").
3. **Draft the body** using the template above. Review against the Principles —
   especially that the problem and solution are separated and scope stays lean.
4. **Check for duplicates before filing.** Search existing issues so you do not
   create a duplicate:

   ```bash
   gh issue list --search "<keywords from the title>" --state all
   ```

   If a matching issue already exists, update or comment on it instead of filing a new one.
5. **File the issue** with the `gh` CLI:

   ```bash
   gh issue create --title "<title>" --body-file <path-to-body.md>
   ```

   Prefer `--body-file` over an inline `--body` so multi-line Markdown is preserved.
6. **Verify it was created.** Confirm the issue exists and capture its URL/number:

   ```bash
   gh issue list --search "<title>" --state open
   ```

   Only retry `gh issue create` if this verification shows the issue was **not** created.
   Re-running blindly risks duplicates — always check first.

## Notes

- Keep environment-specific values (repo names, tokens, org-specific URLs) out of the
  drafted content; let `gh` infer the target repo from the current checkout, or pass
  `--repo <owner/repo>` at invocation time rather than hardcoding it.
- `gh` must be authenticated (`gh auth status`) and run from within the target
  repository, or with an explicit `--repo` flag.
