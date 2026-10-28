#!/usr/bin/env python3
"""Find Zoho Analytics v2 code that still uses the removed cross-organization API.

Every pattern comes from migration-map.json — this script holds no facts of its own.

    python3 scan.py /path/to/your/project          report every hit
    python3 scan.py /path/to/your/project --json   machine-readable, for an agent
    python3 scan.py --self-check                   verify the map against the chapters

Exits 1 when anything of severity "error" is found, so it works as a CI gate.
No third-party dependencies — standard library only, same as build.py.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAP_FILE = HERE / "migration-map.json"
CHAPTERS = HERE.parent

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "venv", ".venv", "env",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".tox", ".gradle", ".idea",
    ".vscode", "dist", "build", "target", "out", "bin", "obj", "coverage",
    ".next", ".nuxt", ".terraform", "site-packages",
}

# Worth scanning: source, config, docs and collections. Everything a stale
# endpoint can hide in, including the artefacts chapter 05 lists.
SCAN_SUFFIXES = {
    ".java", ".py", ".cs", ".go", ".php", ".js", ".jsx", ".ts", ".tsx", ".rb",
    ".kt", ".scala", ".swift", ".c", ".cpp", ".h", ".rs", ".dg", ".ds",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".properties", ".env",
    ".md", ".mdx", ".rst", ".txt", ".adoc", ".html", ".htm",
    ".sh", ".bash", ".zsh", ".ps1", ".sql", ".tf", ".gradle",
}

MAX_BYTES = 4 * 1024 * 1024  # skip anything bigger; it is not hand-written code

COLOR = sys.stdout.isatty()


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def load_map() -> dict:
    try:
        return json.loads(MAP_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: {MAP_FILE} not found")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {MAP_FILE} is not valid JSON — {exc}")


def compile_patterns(data: dict) -> list[dict]:
    out = []
    for p in data["scan_patterns"]["patterns"]:
        try:
            p = dict(p, compiled=re.compile(p["regex"]))
        except re.error as exc:
            sys.exit(f"error: pattern {p['id']} has an invalid regex — {exc}")
        out.append(p)
    return out


def walk(root: Path):
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                continue
        except OSError:
            continue
        yield path


def scan(root: Path, patterns: list[dict]) -> list[dict]:
    findings = []
    for path in walk(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        # Cheap reject: nothing in the map can match a file with no mention
        # of the API surface at all.
        if "restapi/v2" not in text and "Workspaces" not in text \
                and "workspaces" not in text and "ashboard" not in text \
                and "ecent" not in text and "Orgs" not in text and "orgs" not in text:
            continue
        lines = text.splitlines()
        for number, line in enumerate(lines, start=1):
            if len(line) > 2000:
                line = line[:2000]
            for pattern in patterns:
                if pattern["compiled"].search(line):
                    findings.append({
                        "file": str(path),
                        "line": number,
                        "text": line.strip()[:200],
                        "pattern": pattern["id"],
                        "severity": pattern["severity"],
                        "message": pattern["message"],
                        "chapter": pattern["chapter"],
                    })
    return findings


def report(findings: list[dict], root: Path, data: dict) -> None:
    deadline = data["deadline"]["removal"]
    if not findings:
        print(paint("✓ No deprecated Zoho Analytics v2 usage found.", "32"))
        print(f"  Scanned: {root}")
        return

    errors = [f for f in findings if f["severity"] == "error"]
    warns = [f for f in findings if f["severity"] != "error"]

    by_pattern: dict[str, list[dict]] = {}
    for f in findings:
        by_pattern.setdefault(f["pattern"], []).append(f)

    print(f"Scanned: {root}")
    print(f"Found {len(findings)} occurrence(s) across {len(by_pattern)} issue type(s).")
    print(f"The removed endpoints stop answering in {paint(deadline, '1;33')}.\n")

    for pattern_id, group in by_pattern.items():
        severity = group[0]["severity"]
        tag = paint("ERROR", "1;31") if severity == "error" else paint("WARN ", "1;33")
        print(f"{tag} {paint(pattern_id, '1')}  ({len(group)} occurrence(s))")
        print(f"      {group[0]['message']}")
        print(f"      → {group[0]['chapter']}")
        for f in group[:20]:
            print(f"        {f['file']}:{f['line']}  {f['text']}")
        if len(group) > 20:
            print(f"        … and {len(group) - 20} more")
        print()

    print(f"{len(errors)} error(s), {len(warns)} warning(s).")
    if warns:
        print("Warnings are usually fine if the call is already on an OrgAPI or "
              "WorkspaceAPI instance — check each one.")


def self_check(data: dict) -> int:
    """Verify the map still agrees with the chapters it was derived from.

    This is the drift guard. The chapters are the source of truth; if the map
    claims an endpoint or method the prose has never heard of, the map is stale.
    """
    problems: list[str] = []

    chapter_text: dict[str, str] = {}
    for key, meta in data["chapters"].items():
        path = CHAPTERS / meta["file"]
        if not path.exists():
            problems.append(f"chapter {key}: {meta['file']} does not exist")
            continue
        chapter_text[key] = path.read_text(encoding="utf-8")

    everything = "\n".join(chapter_text.values())

    # 1. The deadline must match build.py's single constant.
    build_py = CHAPTERS / "build.py"
    if build_py.exists():
        match = re.search(r'REMOVAL_DEADLINE\s*=\s*"([^"]+)"', build_py.read_text(encoding="utf-8"))
        if not match:
            problems.append("build.py: REMOVAL_DEADLINE not found")
        elif match.group(1) != data["deadline"]["removal"]:
            problems.append(
                f"deadline drift: map says {data['deadline']['removal']!r}, "
                f"build.py says {match.group(1)!r}"
            )
    else:
        problems.append("build.py not found — cannot verify the deadline")

    # 2. Every old and new endpoint path in the map must appear in the prose.
    for entry in data["endpoints"]["replaced"]:
        old_path = entry["old"].split(" ", 1)[1]
        if old_path not in everything:
            problems.append(f"endpoint {old_path} is in the map but in no chapter")
        if entry["new"]:
            new_path = entry["new"].split(" ", 1)[1]
            if new_path not in everything:
                problems.append(f"replacement {new_path} is in the map but in no chapter")

    for entry in data["endpoints"]["new"]:
        if entry["path"] not in everything:
            problems.append(f"new endpoint {entry['path']} is in the map but in no chapter")

    # 3. Every SDK method name in the map must appear in chapter 04.
    sdk_text = chapter_text.get("04", "")
    for entry in data["sdk"]["method_map"]:
        if entry["old"] not in sdk_text:
            problems.append(f"SDK method {entry['old']} is in the map but not in chapter 04")
        if entry.get("new") and entry["new"] not in sdk_text:
            problems.append(f"SDK method {entry['new']} is in the map but not in chapter 04")

    # 4. Every error code in the map must appear somewhere in the prose.
    for entry in data["error_codes"]:
        if str(entry["code"]) not in everything:
            problems.append(f"error code {entry['code']} is in the map but in no chapter")

    # 5. Every chapter anchor the patterns point at must resolve.
    for pattern in data["scan_patterns"]["patterns"]:
        target = pattern["chapter"]
        file_part, _, anchor = target.partition("#")
        path = CHAPTERS / file_part
        if not path.exists():
            problems.append(f"pattern {pattern['id']}: {file_part} does not exist")
            continue
        if anchor:
            body = path.read_text(encoding="utf-8")
            slugs = {slugify(h) for h in re.findall(r"^#{2,4}\s+(.+)$", body, re.M)}
            if anchor not in slugs:
                problems.append(f"pattern {pattern['id']}: #{anchor} does not resolve in {file_part}")

    # 6. The patterns must actually fire on the chapters' own "Before" examples.
    for pattern in data["scan_patterns"]["patterns"]:
        if not re.compile(pattern["regex"]).search(everything):
            problems.append(f"pattern {pattern['id']} matches nothing in the guide — probably dead")

    if problems:
        print(paint(f"✗ {len(problems)} problem(s):", "1;31"))
        for problem in problems:
            print(f"  - {problem}")
        return 1

    counts = (
        f"{len(data['endpoints']['replaced'])} replaced endpoints, "
        f"{len(data['sdk']['method_map'])} SDK methods, "
        f"{len(data['error_codes'])} error codes, "
        f"{len(data['scan_patterns']['patterns'])} scan patterns"
    )
    print(paint("✓ migration-map.json agrees with the chapters.", "32"))
    print(f"  {counts}")
    return 0


def slugify(heading: str) -> str:
    """Mirror build.py: strip a leading section number, then slug the rest."""
    heading = re.sub(r"^\d+\.\s*", "", heading.strip())
    heading = re.sub(r"`([^`]*)`", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.replace("&mdash;", "").replace("—", "")
    heading = re.sub(r"[^\w\s-]", "", heading.lower())
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find Zoho Analytics v2 code using the removed cross-organization API.",
    )
    parser.add_argument("path", nargs="?", help="file or directory to scan")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    parser.add_argument("--self-check", action="store_true",
                        help="verify migration-map.json against the chapters")
    args = parser.parse_args()

    data = load_map()

    if args.self_check:
        return self_check(data)

    if not args.path:
        parser.error("a path to scan is required (or use --self-check)")

    root = Path(args.path).resolve()
    if not root.exists():
        sys.exit(f"error: {root} does not exist")

    findings = scan(root, compile_patterns(data))

    if args.json:
        print(json.dumps({
            "scanned": str(root),
            "deadline": data["deadline"]["removal"],
            "counts": {
                "total": len(findings),
                "error": sum(1 for f in findings if f["severity"] == "error"),
                "warn": sum(1 for f in findings if f["severity"] != "error"),
            },
            "findings": findings,
        }, indent=2))
    else:
        report(findings, root, data)

    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
