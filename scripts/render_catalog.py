#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from catalog import README_PATH, load_projects, render_catalog, render_readme, validate_projects


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the project catalog into README.md")
    parser.add_argument("--check", action="store_true", help="fail if README.md is not current")
    args = parser.parse_args()

    projects = load_projects()
    errors = validate_projects(projects)
    if errors:
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1

    current = README_PATH.read_text(encoding="utf-8")
    rendered = render_readme(current, render_catalog(projects))

    if args.check:
        if rendered != current:
            print("README.md is out of date. Run python3 scripts/render_catalog.py.", file=sys.stderr)
            return 1
        print("README.md is current.")
        return 0

    README_PATH.write_text(rendered, encoding="utf-8")
    print(f"Rendered {len(projects)} projects into README.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
