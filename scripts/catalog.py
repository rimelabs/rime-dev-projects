from __future__ import annotations

import json
import re
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
    "project_type",
    "team_name",
    "event",
    "event_order",
    "source_url",
    "article_url",
    "live_demo_url",
    "demo_video_url",
    "summary",
    "team_members",
}
PROJECT_TYPES = {
    "Application",
    "Integration",
    "Adapter",
    "Evaluation resource",
    "Developer tool",
    "Reference example",
}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

GITHUB_BADGE = "https://badges.aleen42.com/src/github.svg"
YOUTUBE_BADGE = "https://badges.aleen42.com/src/youtube.svg"
DRIVE_BADGE = (
    "https://img.shields.io/badge/Google_Drive-4285F4"
    "?style=flat&logo=googledrive&logoColor=white"
)
VIDEO_BADGE = (
    "https://img.shields.io/badge/Watch-demo-6E56CF"
    "?style=flat&logo=playstation&logoColor=white"
)
LIVE_BADGE = (
    "https://img.shields.io/badge/Try_live-4F46E5"
    "?style=flat&logo=googlechrome&logoColor=white"
)
LINKEDIN_BADGE = (
    "https://img.shields.io/badge/LinkedIn-0A66C2"
    "?style=flat&logo=linkedin&logoColor=white"
)


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
    event_orders: set[tuple[str, int]] = set()

    if not projects:
        return ["The catalog must contain at least one project."]

    for index, project in enumerate(projects, start=1):
        label = project.get("slug") or f"entry {index}"
        missing = REQUIRED_FIELDS - set(project)
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}")
            continue

        slug = project["slug"]
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
            errors.append(f"{label}: slug must contain lowercase letters, numbers, and single hyphens")
        else:
            if slug in slugs:
                errors.append(f"{label}: duplicate slug")
            slugs.add(slug)

        for field in ("name", "team_name", "event"):
            value = project[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}: {field} must be a non-empty string")

        if not isinstance(project["event_order"], int) or project["event_order"] < 1:
            errors.append(f"{label}: event_order must be a positive integer")
        elif isinstance(project["event"], str):
            event_key = (project["event"], project["event_order"])
            if event_key in event_orders:
                errors.append(f"{label}: duplicate event_order for {project['event']}")
            event_orders.add(event_key)

        if not isinstance(project["project_type"], str) or project["project_type"] not in PROJECT_TYPES:
            allowed = ", ".join(sorted(PROJECT_TYPES))
            errors.append(f"{label}: project_type must be one of: {allowed}")

        if not is_http_url(project["source_url"]):
            errors.append(f"{label}: source_url must be an HTTP(S) URL")

        for field in ("article_url", "live_demo_url", "demo_video_url"):
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
            if not member.get("linkedin") and not member.get("github"):
                errors.append(f"{member_label}: a LinkedIn or GitHub URL is required")
            for field in ("linkedin", "github"):
                value = member.get(field)
                if value is not None and not is_http_url(value):
                    errors.append(f"{member_label}: {field} must be null or an HTTP(S) URL")

    return errors


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def image_link(label: str, url: str, image_url: str, *, height: int | None = None) -> str:
    size = f' height="{height}"' if height else ""
    return f'<a href="{url}"><img src="{image_url}" alt="{label}"{size}></a>'


def render_project(project: dict) -> str:
    return f"**{escape_cell(project['name'])}**"


def render_repository(url: str) -> str:
    repository_name = urlparse(url).path.strip("/")
    return (
        f"[{escape_cell(repository_name)}]({url})<br>"
        f"{image_link('View source on GitHub', url, GITHUB_BADGE)}"
    )


def render_demo(live_url: str | None, video_url: str | None) -> str:
    links: list[str] = []
    if live_url:
        links.append(image_link("Try the live demo", live_url, LIVE_BADGE))

    if not video_url:
        return "<br>".join(links)
    hostname = urlparse(video_url).netloc.lower()
    if "youtu.be" in hostname or "youtube.com" in hostname:
        badge = YOUTUBE_BADGE
        label = "Watch on YouTube"
    elif "drive.google.com" in hostname:
        badge = DRIVE_BADGE
        label = "Watch on Google Drive"
    else:
        badge = VIDEO_BADGE
        label = "Watch the demo"
    links.append(image_link(label, video_url, badge))
    return "<br>".join(links)


def render_team(project: dict) -> str:
    members: list[str] = []
    for member in project["team_members"]:
        if member.get("linkedin"):
            profile = image_link(
                f"{member['name']} on LinkedIn",
                member["linkedin"],
                LINKEDIN_BADGE,
                height=16,
            )
        elif member.get("github"):
            profile = image_link(
                f"{member['name']} on GitHub",
                member["github"],
                GITHUB_BADGE,
                height=16,
            )
        else:
            profile = ""
        member_name = escape_cell(member["name"]).replace(" ", "&nbsp;")
        members.append(f"•&nbsp;{member_name}&nbsp;{profile}".rstrip())
    return f"**{escape_cell(project['team_name'])}**<br>" + " ".join(members)


def render_catalog(projects: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {}
    for project in projects:
        grouped.setdefault(project["event"], []).append(project)

    chunks: list[str] = []
    for event, event_projects in grouped.items():
        chunks.extend(
            [
                "",
                f"### {escape_cell(event)}",
                "",
                "| Project | What it does | Repository | Demo | Team members |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for project in sorted(event_projects, key=lambda item: item["event_order"]):
            chunks.append(
                "| "
                + " | ".join(
                    [
                        render_project(project),
                        escape_cell(project["summary"]),
                        render_repository(project["source_url"]),
                        render_demo(project["live_demo_url"], project["demo_video_url"]),
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
