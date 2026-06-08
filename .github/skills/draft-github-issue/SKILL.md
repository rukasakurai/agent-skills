---
name: draft-github-issue
description: 'File a GitHub issue from a bug report, discussion, or analysis using the gh CLI. Use to create, draft, or open a problem-focused issue that stays lean and leaves implementation freedom to the assignee.'
argument-hint: Describe the problem or paste the discussion to turn into an issue
---

# Draft GitHub Issue

## When to Use

- You have a discussion, investigation, or code analysis that should become a tracked issue.
- You want an issue that clearly states the problem without over-prescribing the solution.

## Principles

- Separate the problem from the solution.
- Keep it lean.
- State constraints, then leave implementation freedom to the assignee within them.
- Title states the problem, not the solution (e.g. "Parser rejects valid UTF-8 input", not "Add UTF-8 validation").

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

1. **File the issue** with the `gh` CLI, using inline `--body` with a here-doc (via command substitution) to
   preserve multi-line Markdown:

   ```bash
   gh issue create --title "<title>" --body "$(cat <<'EOF'
   ## Problem

   ...

   ## Desired behavior

   ...

   ## Constraints

   ...
   EOF
   )"
   ```

2. **Verify before retrying.** Confirm the issue exists and capture its URL/number:

   ```bash
   gh issue list --search "<title>" --state open
   ```

   Only retry `gh issue create` if this verification shows the issue was **not**
   created. Re-running blindly risks duplicates — always check first.
