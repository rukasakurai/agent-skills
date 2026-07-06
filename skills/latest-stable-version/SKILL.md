---
name: latest-stable-version
description: 'Verify and select the latest stable (non-preview) release before pinning or bumping a dependency version — ARM/Bicep API versions, NuGet, npm, PyPI, Go modules, or container images. Use when adding or changing a pinned version, or when reviewing a change that pins one, to avoid shipping outdated or preview versions.'
argument-hint: Name the dependency (and ecosystem) whose version you are pinning or reviewing
---

# Latest Stable Version

## When to Use

- You are about to pin or bump a version: an ARM/Bicep API version, a NuGet/npm/PyPI/Go package, an SDK, or a container base image.
- You are reviewing a change that pins a version and want to confirm it is current.

## Rule

Pick the **latest stable** release. Treat SemVer pre-releases (anything after the first `-`, e.g. `-rc.1`, `-beta`, `-alpha`, `-dev`) and ecosystem-specific preview markers (e.g. ARM `-preview`, PyPI `a`/`b`/`rc`/`.dev`) as **not stable**.

Use an older or preview version only with an explicit, written reason (e.g. a feature exists only in preview, or a newer stable breaks a required contract).

A version change is a behavior change: **re-run the relevant build and tests** after bumping.

## Verify Before Pinning

Look up the current versions with the per-ecosystem command, then choose the highest stable version (excluding pre-releases).

| Ecosystem | Command |
| --- | --- |
| npm | `npm view <pkg> version` (latest stable) · `npm view <pkg> versions` (all) |
| PyPI | `pip index versions <pkg>` |
| NuGet | `curl -s https://api.nuget.org/v3-flatcontainer/<pkg-lowercase>/index.json` |
| Go modules | `go list -m -versions <module>` · `go list -m <module>@latest` |
| ARM/Bicep API version | `az provider show --namespace <Namespace> --query "resourceTypes[?resourceType=='<type>'].apiVersions" -o tsv` |
| Container image | `crane ls <repo>` or `skopeo list-tags docker://<repo>` |

Notes:

- **NuGet** returns a JSON `versions` array in ascending order; the last entry without a `-` suffix is the latest stable.
- **ARM/Bicep** stable API versions are plain dates (`2024-10-01`); anything ending in `-preview` is not stable.
- **Container images** — prefer an immutable stable tag over `latest`; pin by digest when reproducibility matters.

## When Reviewing

Flag any pin that is not the latest stable and lacks a stated reason. Run the matching command above to confirm, and ask for justification when a preview or older version is used.
