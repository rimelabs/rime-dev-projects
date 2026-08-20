#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

from catalog import (
    DATA_PATH,
    README_PATH,
    load_projects,
    render_catalog,
    render_readme,
    validate_projects,
)


DEFAULT_EVENT = "Community projects"
REQUIRED_INPUT_FIELDS = {
    "name",
    "project_type",
    "team_name",
    "source_url",
    "summary",
    "team_members",
}
OPTIONAL_INPUT_FIELDS = {
    "slug",
    "event",
    "article_url",
    "live_demo_url",
    "demo_video_url",
}
INPUT_FIELDS = REQUIRED_INPUT_FIELDS | OPTIONAL_INPUT_FIELDS
MEMBER_FIELDS = {"name", "linkedin", "github"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if not slug:
        raise ValueError("The project name cannot produce a valid slug. Supply a slug in the input file.")
    return slug


def normalize_members(raw_members: object) -> list[dict]:
    if not isinstance(raw_members, list) or not raw_members:
        raise ValueError("team_members must contain at least one member.")

    members: list[dict] = []
    for index, raw_member in enumerate(raw_members, start=1):
        if not isinstance(raw_member, dict):
            raise ValueError(f"team member {index} must be an object.")
        unknown = set(raw_member) - MEMBER_FIELDS
        if unknown:
            fields = ", ".join(sorted(unknown))
            raise ValueError(f"team member {index} has unknown fields: {fields}")
        members.append(
            {
                "name": raw_member.get("name"),
                "linkedin": raw_member.get("linkedin"),
                "github": raw_member.get("github"),
            }
        )
    return members


def normalize_project(raw: object, projects: list[dict]) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("The input file must contain one JSON object.")

    unknown = set(raw) - INPUT_FIELDS
    if unknown:
        fields = ", ".join(sorted(unknown))
        raise ValueError(f"The input file has unknown fields: {fields}")

    missing = REQUIRED_INPUT_FIELDS - set(raw)
    if missing:
        fields = ", ".join(sorted(missing))
        raise ValueError(f"The input file is missing fields: {fields}")

    name = raw["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string.")

    slug = raw.get("slug") or slugify(name)
    if any(project.get("slug") == slug for project in projects):
        raise ValueError(f"The slug '{slug}' already exists.")

    event = raw.get("event") or DEFAULT_EVENT
    event_orders = [
        project["event_order"]
        for project in projects
        if project.get("event") == event and isinstance(project.get("event_order"), int)
    ]

    return {
        "slug": slug,
        "name": name.strip(),
        "project_type": raw["project_type"],
        "team_name": raw["team_name"],
        "event": event,
        "event_order": max(event_orders, default=0) + 1,
        "source_url": raw["source_url"],
        "article_url": raw.get("article_url"),
        "demo_video_url": raw.get("demo_video_url"),
        "live_demo_url": raw.get("live_demo_url"),
        "summary": raw["summary"],
        "team_members": normalize_members(raw["team_members"]),
    }


def load_input(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Input file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Input file is not valid JSON: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add one project to the catalog, calculate its ordering, and render the README."
    )
    parser.add_argument("--file", required=True, type=Path, help="JSON file that follows data/project.schema.json")
    parser.add_argument("--dry-run", action="store_true", help="print the normalized project without changing files")
    args = parser.parse_args()

    try:
        projects = load_projects()
        project = normalize_project(load_input(args.file), projects)
        updated_projects = [*projects, project]
        errors = validate_projects(updated_projects)
        if errors:
            raise ValueError("\n".join(errors))

        serialized_project = json.dumps(project, ensure_ascii=False, indent=2)
        if args.dry_run:
            print(serialized_project)
            return 0

        rendered_readme = render_readme(
            README_PATH.read_text(encoding="utf-8"),
            render_catalog(updated_projects),
        )
        DATA_PATH.write_text(json.dumps(updated_projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        README_PATH.write_text(rendered_readme, encoding="utf-8")
        print(f"Added {project['name']} as {project['slug']} in {project['event']}.")
        print("Run just check, review the diff, and open a pull request.")
        return 0
    except ValueError as error:
        print(f"Cannot add project: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
