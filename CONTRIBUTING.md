# Contributing

Thanks for helping us document and share what developers build with Rime.

## Project requirements

A project is eligible when:

- it is a voice application, integration, adapter, evaluation resource, or other reusable developer tool built at an event or independently by the community;
- Rime is a meaningful part of the project, or the work is directly useful to developers building with Rime;
- its source repository is public and contains enough information to understand the implementation; and
- the public repository does not contain live credentials, private data, or other secrets.

Articles and demo videos are encouraged but not required. LinkedIn URLs should be supplied by the builders themselves or taken from a public profile they control. Do not guess a person’s profile from their name.

## Add a project

1. Add one object to [`data/projects.json`](data/projects.json).
2. Run `python3 scripts/render_catalog.py` to update the README.
3. Run `python3 scripts/check_catalog.py`.
4. Open a pull request describing where the project came from and how it uses or supports Rime.

For an independent submission, use `Community projects` as the event. Use `null` for an unavailable article, demo video, or LinkedIn URL. Keep the executive summary to one or two concrete sentences. Describe what the project does, how Rime is used, and why the work is useful; avoid unsupported performance or quality claims.

## Update builder information

Builders are welcome to add or correct their names and LinkedIn profiles through an issue or pull request. A GitHub profile is used as a temporary fallback when a LinkedIn URL has not been provided.
