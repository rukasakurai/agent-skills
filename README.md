# agent-skills

Reusable agent skills that can be installed across repositories and machines.

## Skills

| Skill | Description |
| --- | --- |
| [`draft-github-issue`](.github/skills/draft-github-issue/SKILL.md) | Turn a discussion or code analysis into a lean, problem-focused GitHub issue and file it with the `gh` CLI. |

## Layout

Each skill lives in its own folder under `.github/skills/<skill-name>/` with a
`SKILL.md` whose `name` matches the folder name.