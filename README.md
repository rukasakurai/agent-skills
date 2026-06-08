# agent-skills

Reusable agent skills that can be installed across repositories and machines.

## Skills

| Skill | Description |
| --- | --- |
| [`draft-github-issue`](.github/skills/draft-github-issue/SKILL.md) | Turn a discussion or code analysis into a lean, problem-focused GitHub issue and file it with the `gh` CLI. |

## Install

Install a skill with the [`gh skill`](https://cli.github.com/manual/gh_skill_install)
command (requires GitHub CLI v2.90.0+):

```sh
# Install into the current repository (project scope)
gh skill install rukasakurai/agent-skills draft-github-issue

# Install for use everywhere (user scope)
gh skill install rukasakurai/agent-skills draft-github-issue --scope user
```

By default skills install for GitHub Copilot. Use `--agent` to target another
agent (for example `--agent claude-code`), and `--pin <tag-or-sha>` to lock to a
specific version.

## Update

Installed skills carry source metadata, so [`gh skill update`](https://cli.github.com/manual/gh_skill_update)
can detect and apply upstream changes:

```sh
# Check for updates interactively
gh skill update

# Update a specific skill
gh skill update draft-github-issue

# Update everything without prompting
gh skill update --all

# Preview available updates without changing files
gh skill update --dry-run
```

## Layout

Each skill lives in its own folder under `.github/skills/<skill-name>/` with a
`SKILL.md` whose `name` matches the folder name.