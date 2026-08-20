# Agent guide

This repository is a catalog. Project source code stays in each builder's repository.

## Source of truth

- Add and update project metadata in `data/projects.json`.
- Use `data/project.example.json` as the input template.
- Use `data/project.schema.json` as the machine-readable input contract.
- Do not edit the project table in `README.md` by hand.
- Keep both `<!-- PROJECTS:START -->` and `<!-- PROJECTS:END -->` in the README.

## Add a project

1. Examine the source repository and use only facts that it contains.
2. Do not invent demo links, team profiles, performance claims, or affiliations.
3. Copy `data/project.example.json` to a temporary file and update its values.
4. Run `just add /path/to/project.json`.
5. Run `just check`.
6. Review the generated README row and the full diff.
7. Open a pull request. Do not push directly to `main`.

The add script creates the slug and event order. It also updates the generated README table.

## Contribution policy

- Voice must be a meaningful part of the project, or the work must help voice AI developers.
- Rime is encouraged but not required.
- The source repository must be public and must not contain credentials or private data.
- Use builder profile links only when the builders supplied them or control the linked profiles.

## Commands

```bash
just add /path/to/project.json
just render
just test
just check
```
