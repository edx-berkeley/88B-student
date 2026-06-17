#!/usr/bin/env python3
"""
Sync myst.yml TOC with DATA 88B lab notebooks on disk.
Finds lab/N/labNN/labNN.ipynb for N in {1,2,3}, builds the table of contents
in order, and updates myst.yml.
Run from repository root. Exits 0 if no change, 2 on error.
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
MYST_PATH = REPO_ROOT / "myst.yml"

EXIT_SUCCESS = 0
EXIT_ERROR = 2

PART_TITLES = {
    "1": "Part 1 - Data Exploration",
    "2": "Part 2 - Inferential Statistics",
    "3": "Part 3 - Linear Regression",
}


def notebook_title(nb_path: Path) -> str | None:
    """Return the first markdown H1 heading from a notebook, if present."""
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Warning: could not read {nb_path}: {e}", file=sys.stderr)
        return None

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        text = "".join(source) if isinstance(source, list) else source
        match = re.match(r"^#\s+(.+?)\s*$", text.strip(), re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def find_part_labs(part: str) -> list[dict]:
    """Find all labNN/labNN.ipynb under lab/part/, sorted by NN."""
    base = REPO_ROOT / "lab" / part
    if not base.is_dir():
        return []
    pattern = re.compile(r"^lab(\d+)$")
    entries = []
    for path in sorted(base.iterdir()):
        if not path.is_dir():
            continue
        m = pattern.match(path.name)
        if not m:
            continue
        num = m.group(1)
        nb = path / f"{path.name}.ipynb"
        if nb.is_file():
            rel = str(nb.relative_to(REPO_ROOT)).replace("\\", "/")
            title = notebook_title(nb) or f"Lab {num.zfill(2)}"
            entries.append({"title": title, "file": rel})
    entries.sort(key=lambda e: int(re.search(r"lab(\d+)", e["file"]).group(1)))
    return entries


def main() -> int:
    if not MYST_PATH.is_file():
        print(f"Error: {MYST_PATH} not found", file=sys.stderr)
        return EXIT_ERROR

    toc = []

    intro = REPO_ROOT / "intro.md"
    if intro.exists():
        toc.append({"file": "intro.md"})

    for part in sorted(PART_TITLES):
        labs = find_part_labs(part)
        if labs:
            toc.append({"title": PART_TITLES[part], "children": labs})

    try:
        with open(MYST_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: invalid YAML in {MYST_PATH}: {e}", file=sys.stderr)
        return EXIT_ERROR

    if data is None:
        data = {}
    if "project" not in data:
        data["project"] = {}

    old_toc = data["project"].get("toc", [])
    if old_toc == toc:
        return EXIT_SUCCESS

    data["project"]["toc"] = toc
    with open(MYST_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return EXIT_SUCCESS


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
