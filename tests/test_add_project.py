from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from add_project import normalize_project, slugify  # noqa: E402
from catalog import validate_projects  # noqa: E402


class AddProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "name": "Café Voice",
            "project_type": "Application",
            "team_name": "Example Team",
            "source_url": "https://github.com/example/cafe-voice",
            "summary": "A voice application.",
            "team_members": [
                {
                    "name": "Example Builder",
                    "github": "https://github.com/example",
                }
            ],
        }
        self.projects = [
            {
                "slug": "existing-project",
                "event": "Community projects",
                "event_order": 2,
            }
        ]

    def test_slugify_normalizes_project_name(self) -> None:
        self.assertEqual(slugify("Café Voice"), "cafe-voice")

    def test_normalize_project_adds_defaults(self) -> None:
        project = normalize_project(self.payload, self.projects)

        self.assertEqual(project["slug"], "cafe-voice")
        self.assertEqual(project["event"], "Community projects")
        self.assertEqual(project["event_order"], 3)
        self.assertIsNone(project["live_demo_url"])
        self.assertIsNone(project["demo_video_url"])

    def test_normalize_project_rejects_duplicate_slug(self) -> None:
        payload = {**self.payload, "slug": "existing-project"}

        with self.assertRaisesRegex(ValueError, "already exists"):
            normalize_project(payload, self.projects)

    def test_normalized_project_passes_catalog_validation(self) -> None:
        project = normalize_project(self.payload, [])

        self.assertEqual(validate_projects([project]), [])

    def test_catalog_validation_rejects_missing_profile(self) -> None:
        project = normalize_project(self.payload, [])
        project["team_members"][0]["github"] = None

        self.assertIn(
            "cafe-voice team member 1: a LinkedIn or GitHub URL is required",
            validate_projects([project]),
        )


if __name__ == "__main__":
    unittest.main()
