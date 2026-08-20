python := env_var_or_default("PYTHON", "python3")

# List the available project tasks.
default:
    @just --list

# Add a project from a JSON metadata file.
add project:
    {{ python }} scripts/add_project.py --file "{{ project }}"

# Regenerate the project table in README.md.
render:
    {{ python }} scripts/render_catalog.py

# Run the unit tests.
test:
    {{ python }} -m unittest discover -s tests

# Validate data, generated output, Python syntax, and tests.
check:
    {{ python }} scripts/check_catalog.py
    {{ python }} scripts/render_catalog.py --check
    {{ python }} -m compileall -q scripts
    {{ python }} -m unittest discover -s tests
