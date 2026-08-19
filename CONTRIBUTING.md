# Contributing

Thanks for helping us document and share useful work from the voice AI developer community.

## What we accept

We welcome:

- Voice applications built at developer events or independently by the community
- Integrations and adapters for voice frameworks and developer workflows
- Best practices, evaluation resources, reference examples, and tools for voice AI developers
- Focused technical work with a public repository and enough documentation to understand or run it

Rime does not need to be part of the project. We would love for you to use a Rime voice. If another voice sounds better for your application, we still welcome the contribution. Our goal is to make this repository a useful resource for the voice AI community and inspire more developers to build and share their work.

## What we don't accept

- Projects where voice is not a meaningful part of the application
- Private or inaccessible repositories
- Repositories without enough documentation to understand the implementation
- Submissions containing credentials, private data, or material copied without permission
- Unsupported performance, quality, or comparison claims
- Builder names or profile links submitted without their consent

Articles, live demos, and demo videos are encouraged but not required. LinkedIn URLs should be supplied by the builders themselves or taken from a public profile they control. Do not guess a person’s profile from their name.

## Add a project

1. Add one object to [`data/projects.json`](data/projects.json).
2. Run `python3 scripts/render_catalog.py` to update the README.
3. Run `python3 scripts/check_catalog.py`.
4. Open a pull request that explains where the project came from and how it uses voice.

For an independent submission, use `Community projects` as the event. Choose one of the project types accepted by the catalog validator. Use `null` for an unavailable article, live demo, demo video, or LinkedIn URL. Keep the executive summary to one or two concrete sentences. Describe what the project does, how it uses voice, and why the work is useful.

## Update builder information

Builders are welcome to add or correct their names and LinkedIn profiles through an issue or pull request. A GitHub profile is used as a temporary fallback when a LinkedIn URL has not been provided.

## Community standards

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contribution will be licensed under the [Apache License 2.0](LICENSE).
