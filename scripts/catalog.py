from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "projects.json"
README_PATH = ROOT / "README.md"
START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"
REQUIRED_FIELDS = {
    "slug",
    "name",
    "team_name",
    "event",
    "event_order",
    "source_url",
    "article_url",
    "demo_video_url",
    "summary",
    "team_members",
}


def load_projects() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_projects(projects: list[dict]) -> list[str]:
    errors: list[str] = []
    slugs: set[str] = set()

    if not projects:
        return ["The catalog must contain at least one project."]

    for index, project in enumerate(projects, start=1):
        label = project.get("slug") or f"entry {index}"
        missing = REQUIRED_FIELDS - set(project)
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}")
            continue

        slug = project["slug"]
        if slug in slugs:
            errors.append(f"{label}: duplicate slug")
        slugs.add(slug)

        if not isinstance(project["event_order"], int) or project["event_order"] < 1:
            errors.append(f"{label}: event_order must be a positive integer")

        if not is_http_url(project["source_url"]):
            errors.append(f"{label}: source_url must be an HTTP(S) URL")

        for field in ("article_url", "demo_video_url"):
            value = project[field]
            if value is not None and not is_http_url(value):
                errors.append(f"{label}: {field} must be null or an HTTP(S) URL")

        if not isinstance(project["summary"], str) or not project["summary"].strip():
            errors.append(f"{label}: summary must be non-empty")

        members = project["team_members"]
        if not isinstance(members, list) or not members:
            errors.append(f"{label}: team_members must contain at least one member")
            continue

        for member_index, member in enumerate(members, start=1):
            member_label = f"{label} team member {member_index}"
            if not isinstance(member, dict) or not member.get("name"):
                errors.append(f"{member_label}: name is required")
                continue
            for field in ("linkedin", "github"):
                value = member.get(field)
                if value is not None and not is_http_url(value):
                    errors.append(f"{member_label}: {field} must be null or an HTTP(S) URL")

    return errors


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def link(label: str, url: str | None) -> str:
    return f"[{escape_cell(label)}]({url})" if url else "—"


def render_team(project: dict) -> str:
    members: list[str] = []
    for member in project["team_members"]:
        if member.get("linkedin"):
            members.append(link(member["name"], member["linkedin"]))
        elif member.get("github"):
            members.append(f"{link(member['name'], member['github'])} _(GitHub)_")
        else:
            members.append(escape_cell(member["name"]))
    return f"**{escape_cell(project['team_name'])}**<br>" + " · ".join(members)


def render_catalog(projects: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {}
    for project in projects:
        grouped.setdefault(project["event"], []).append(project)

    event_count = len(grouped)
    event_label = "developer event" if event_count == 1 else "developer events"
    chunks = [f"_Featuring {len(projects)} projects across {event_count} {event_label}._"]
    for event, event_projects in grouped.items():
        chunks.extend(
            [
                "",
                f"### {escape_cell(event)}",
                "",
                "| Project | Brief executive summary | Article / write-up | Demo video | Team members |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for project in sorted(event_projects, key=lambda item: item["event_order"]):
            chunks.append(
                "| "
                + " | ".join(
                    [
                        link(project["name"], project["source_url"]),
                        escape_cell(project["summary"]),
                        link("Read", project["article_url"]),
                        link("Watch", project["demo_video_url"]),
                        render_team(project),
                    ]
                )
                + " |"
            )

    return "\n".join(chunks).rstrip()


def render_readme(current: str, catalog: str) -> str:
    if current.count(START_MARKER) != 1 or current.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one pair of catalog markers")

    before, remainder = current.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return f"{before}{START_MARKER}\n{catalog}\n{END_MARKER}{after}"
