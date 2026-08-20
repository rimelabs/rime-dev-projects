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

Project code stays in the builder's repository. This repository stores only the catalog entry.

1. Copy [`data/project.example.json`](data/project.example.json) to a temporary file.
2. Replace the example values with facts from the project repository.
3. Install [`just`](https://just.systems/man/en/packages.html) if it is not already available.
4. Run `just add /path/to/project.json`.
5. Run `just check`.
6. Review the generated README row and open a pull request.

For an independent submission, use `Community projects` as the event. Choose one of the project types accepted by the catalog validator. Use `null` for an unavailable article, live demo, demo video, or LinkedIn URL. Keep the executive summary to one or two concrete sentences. Describe what the project does, how it uses voice, and why the work is useful.

The add script creates the slug and event order. The input format is defined in [`data/project.schema.json`](data/project.schema.json).

### External CLI workflow

Contributors without write access can use a fork:

```bash
gh repo fork rimelabs/rime-dev-projects --clone
cd rime-dev-projects
git switch -c add-project-name
cp data/project.example.json /tmp/project.json
# Edit /tmp/project.json with project details.
just add /tmp/project.json
just check
git add data/projects.json README.md
git commit -m "Add project name"
git push -u origin add-project-name
gh pr create --fill
```

If you edit `data/projects.json` directly, run `just render` before `just check`. Do not edit the generated README table by hand.

## Update builder information

Builders are welcome to add or correct their names and LinkedIn profiles through an issue or pull request. A GitHub profile is used as a temporary fallback when a LinkedIn URL has not been provided.

## Community standards

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contribution will be licensed under the [Apache License 2.0](LICENSE).
