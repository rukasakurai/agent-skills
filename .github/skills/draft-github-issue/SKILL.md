---
name: draft-github-issue
description: 'Turn a discussion or analysis into a GitHub issue filed with the gh CLI. Use when capturing a problem as a lean, problem-focused issue that leaves implementation freedom to the assignee.'
argument-hint: 'Describe the problem or paste the discussion to turn into an issue'
---

# Draft GitHub Issue

Turn a discussion, bug report, or code analysis into a lean, problem-focused GitHub
issue and file it with the `gh` CLI.

## When to Use

- You have a discussion, investigation, or code analysis that should become a tracked issue.
- You want an issue that clearly states the problem without over-prescribing the solution.

## Principles

- Separate the problem from the solution.
- Keep it lean.
- State constraints, then leave implementation freedom to the assignee within them.

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

1. **File the issue** with the `gh` CLI, using inline `--body` with a here-string to
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
