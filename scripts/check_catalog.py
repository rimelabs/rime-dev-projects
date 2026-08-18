#!/usr/bin/env python3
from __future__ import annotations

import sys

from catalog import load_projects, validate_projects


def main() -> int:
    projects = load_projects()
    errors = validate_projects(projects)
    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1

    print(f"Catalog is valid: {len(projects)} projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
