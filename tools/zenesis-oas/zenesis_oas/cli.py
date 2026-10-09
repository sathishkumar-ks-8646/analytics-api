"""
zenesis-oas -- move OpenAPI documents between their Zenesis source form and
the clean, vendor-neutral form that is published, in either direction, and
compare the two.

Two sides, named the same way in every command:

    ZENESIS    the Zenesis-flavoured source, with the x-zenesis-* keys.
               <repo>/vN.N/zenesis-oas/  (or its common/)
    ANALYTICS  the clean, vendor-neutral OpenAPI that is published.
               <repo>/vN.N/oas/                      (or its common/)

Every command reads left to right -- the first path is where the content comes
from, the second is where it goes:

    zenesis-oas to-analytics ZENESIS ANALYTICS            write clean OpenAPI (alias: convert)
    zenesis-oas to-zenesis   ANALYTICS ZENESIS --in-place carry edits back into the source
    zenesis-oas compare      ZENESIS ANALYTICS            what differs; writes nothing
    zenesis-oas inventory    ZENESIS                      which vendor keys are in use
    zenesis-oas overlay      ZENESIS --out overlays/      regenerate the audit overlays
    zenesis-oas verify       ZENESIS --overlays overlays/ prove the conversion is lossless

`to-zenesis` is the one command whose second path is read as well as written:
the Zenesis document is the base of a three-way merge, and `--in-place` writes
the merged result back over it. Use `--out` to write somewhere else and leave
the source untouched.

Each path may be a single .json file or a directory; two directories are
paired file by file on name.

Exit codes:  0 success  |  1 warnings, differences or verification failure  |  2 usage error
"""

import argparse
import json
import pathlib
import re
import sys

from . import overlay as overlaymod
from . import rules as rulesmod
from .converter import convert, inventory
from .report import Report
from .reverse import compare, reverse

LIVE_KEYS = ("x-zenesis-usecase-tag", "x-zenesis-doc")
DEFAULT_RULES_FILE = "rules.json"


# --------------------------------------------------------------------- io

def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_json(path):
    return json.loads(read_text(path))


def detect_format(text):
    """
    (indent, trailing_newline) of an existing file, so a document written
    back over it produces a diff of the edit and nothing else.
    """
    match = re.search(r"\n( +)\"", text)
    indent = len(match.group(1)) if match else 2
    return indent, text.endswith("\n")


def write_json(path, payload, indent=2, trailing_newline=True):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=indent, ensure_ascii=False)
        if trailing_newline:
            handle.write("\n")


def collect(source):
    """Resolve a file or directory argument to a sorted list of .json paths."""
    src = pathlib.Path(source)
    if src.is_dir():
        return sorted(src.glob("*.json"))
    if src.is_file():
        return [src]
    raise FileNotFoundError("no such file or directory: %s" % source)


def pair(left, right):
    """
    Match two file-or-directory arguments into (left_path, right_path) pairs.

    Two files pair with each other whatever their names. Two directories pair
    on file name, and the names found on one side only are returned so the
    caller can say so.
    """
    left_paths, right_paths = collect(left), collect(right)
    left_dir, right_dir = pathlib.Path(left).is_dir(), pathlib.Path(right).is_dir()

    if not left_dir and not right_dir:
        return [(left_paths[0], right_paths[0])], [], []
    if left_dir != right_dir:
        raise ValueError("%s and %s must both be files or both be directories"
                         % (left, right))

    by_name = {p.name: p for p in right_paths}
    pairs = [(p, by_name[p.name]) for p in left_paths if p.name in by_name]
    only_left = [p for p in left_paths if p.name not in by_name]
    left_names = {p.name for p in left_paths}
    only_right = [p for p in right_paths if p.name not in left_names]
    return pairs, only_left, only_right


def note(*parts):
    print(*parts, file=sys.stderr)


def short(value, width=100):
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= width else text[: width - 3] + "..."


def load_rules(args):
    """`--rules FILE`, else ./rules.json when present, else the built-in rules."""
    if args.rules:
        return rulesmod.load_rules(args.rules)
    if pathlib.Path(DEFAULT_RULES_FILE).is_file():
        return rulesmod.load_rules(DEFAULT_RULES_FILE)
    return rulesmod.load_rules()


# --------------------------------------------------------------- commands

def cmd_inventory(args):
    """List every vendor extension across the input specs, before converting."""
    config = load_rules(args)
    prefix = config.get("vendor_prefix", "x-zenesis-")
    known = set(config["rules"])

    totals, examples, unknown = {}, {}, set()

    for path in collect(args.source):
        found = inventory(read_json(path), prefix)
        for key, info in found.items():
            totals[key] = totals.get(key, 0) + info["count"]
            examples.setdefault(key, "%s  %s" % (path.name, info["example"]))
            if key not in known:
                unknown.add(key)

    if not totals:
        note("No %s* extensions found." % prefix)
        return 0

    width = max(len(k) for k in totals)
    note("")
    note("VENDOR EXTENSIONS FOUND")
    note("-" * 74)
    for key in sorted(totals, key=lambda k: -totals[key]):
        flag = "  <-- NOT IN rules.json" if key in unknown else ""
        note("  %-*s  %4d%s" % (width, key, totals[key], flag))
        note("      e.g. %s" % examples[key])
    note("-" * 74)

    if unknown:
        note("")
        note("%d key(s) have no rule. Add them to rules.json before converting,"
             % len(unknown))
        note("or they will be dropped with a warning.")
        return 1
    note("")
    note("Every key has a rule. Safe to convert.")
    return 0


def banner(*lines):
    """
    State the direction before doing anything, so it is never in doubt.
    Each line is (label, path, what-it-is); a repeated label is shown blank.
    """
    note("")
    seen = set()
    for label, path, kind in lines:
        shown = "" if label in seen else label
        seen.add(label)
        note("  %-8s %-46s %s" % (shown, path, kind))
    note("")


def cmd_to_analytics(args):
    """Zenesis source -> clean OpenAPI. The original `convert` command."""
    config = load_rules(args)
    sources = collect(args.source)
    dest = pathlib.Path(args.dest)
    many = len(sources) > 1 or pathlib.Path(args.source).is_dir()

    if not args.quiet:
        banner(("reading", args.source, "the Zenesis source"),
               ("writing", args.dest, "clean OpenAPI"))

    total, failures = Report(), 0

    for path in sources:
        doc, report = convert(read_json(path), config, label=path.name)
        out = dest / path.name if many else dest
        write_json(out, doc, args.indent)

        total.merge(report, prefix="%s  " % path.name)
        if report.warnings:
            failures += 1
        if many and not args.quiet:
            state = ("%d warning(s)" % len(report.warnings)) if report.warnings else "clean"
            note("  %-46s -> %-28s %s" % (path.name, out.name, state))

    if not args.quiet:
        note(total.render())
    if failures and not args.quiet:
        note("")
        note("%d of %d file(s) produced warnings." % (failures, len(sources)))
    return 1 if failures else 0


def cmd_to_zenesis(args):
    """
    Clean OpenAPI edits -> Zenesis source.

    For each pair, the source is converted, the result compared with the
    published document, and every difference written onto the source. The
    merged source is then converted again and compared once more: whatever
    still differs could not be carried and is listed, so nothing is lost
    quietly.
    """
    config = load_rules(args)
    pairs, only_published, only_source = pair(args.published, args.source)
    out_dir = pathlib.Path(args.out) if args.out else None
    many = pathlib.Path(args.source).is_dir()

    banner(("reading", args.published, "clean OpenAPI, for the edits it carries"),
           ("reading", args.source, "the Zenesis source, as the base of the merge"),
           ("writing", args.source if args.in_place else args.out,
            "the merged Zenesis source" + (", in place" if args.in_place else "")))

    total, problems = Report(), 0

    for published_path, source_path in pairs:
        source_text = read_text(source_path)
        base = json.loads(source_text)
        actual = read_json(published_path)

        merged, report = reverse(actual, base, config, label=source_path.name)
        again, _ = convert(merged, config)
        remaining = list(compare(again, actual))

        carried = sum(report.counts.values())
        if args.in_place:
            out = source_path
            if merged != base:
                indent, newline = detect_format(source_text)
                write_json(out, merged, indent, newline)
        else:
            out = out_dir / source_path.name if many else out_dir
            indent, newline = detect_format(source_text)
            write_json(out, merged, indent, newline)

        state = ("%d edit(s) carried" % carried) if carried else "already in step"
        extras = []
        if report.warnings:
            extras.append("%d warning(s)" % len(report.warnings))
        if remaining:
            extras.append("%d difference(s) remain" % len(remaining))
        note("  %-46s %s%s" % (source_path.name, state,
                                (", " + ", ".join(extras)) if extras else ""))
        for where, kind, expected, got in remaining:
            note("      still differs: %s" % where)
            note("          source   : %s" % short(expected))
            note("          published: %s" % short(got))

        total.merge(report, prefix="%s  " % source_path.name)
        if report.warnings or remaining:
            problems += 1

    for path in only_published:
        note("  %-46s no source document of that name to merge into" % path.name)
        problems += 1
    for path in only_source:
        note("  %-46s not in the published set; left as it is" % path.name)

    note(total.render("REVERSE REPORT"))
    if problems:
        note("")
        note("%d file(s) need attention." % problems)
    return 1 if problems else 0


def cmd_compare(args):
    """Convert the source and list where the published document differs."""
    config = load_rules(args)
    pairs, only_source, only_published = pair(args.source, args.published)

    if not args.json:
        banner(("reading", args.source, "the Zenesis source"),
               ("reading", args.published, "clean OpenAPI"),
               ("writing", "-", "nothing; this command only reports"))

    total, results = 0, []
    for source_path, published_path in pairs:
        expected, _ = convert(read_json(source_path), config, label=source_path.name)
        actual = read_json(published_path)
        diffs = list(compare(expected, actual))
        total += len(diffs)

        if args.json:
            results.append({
                "file": source_path.name,
                "differences": [
                    {"path": where, "kind": kind, "source": e, "published": a}
                    for where, kind, e, a in diffs
                ],
            })
            continue

        note("  %-46s %s" % (source_path.name,
                              ("%d difference(s)" % len(diffs)) if diffs else "in step"))
        for where, kind, e, a in diffs:
            note("      %s" % where)
            if kind == "changed":
                note("          source   : %s" % short(e))
                note("          published: %s" % short(a))
            elif kind == "only-in-source":
                note("          only in source   : %s" % short(e))
            else:
                note("          only in published: %s" % short(a))

    for path in only_source:
        note("  %-46s only in the source set" % path.name)
    for path in only_published:
        note("  %-46s only in the published set" % path.name)
    total += len(only_source) + len(only_published)

    if args.json:
        print(json.dumps({"differences": total, "files": results,
                          "only_in_source": [p.name for p in only_source],
                          "only_in_published": [p.name for p in only_published]},
                         indent=2, ensure_ascii=False))
    else:
        note("")
        note("%d difference(s)." % total if total else "No differences.")
    return 1 if total else 0


def cmd_overlay(args):
    """Regenerate the overlays that turn converted output back into the source."""
    config = load_rules(args)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for path in collect(args.source):
        original = read_json(path)
        converted, _ = convert(original, config, label=path.name, rewrite_refs=False)

        live, compat = overlaymod.derive(original, converted, LIVE_KEYS)
        stem = path.stem

        write_json(
            out_dir / ("%s.live.overlay.json" % stem),
            overlaymod.document("Zenesis renderer configuration - %s" % stem, live),
        )
        write_json(
            out_dir / ("%s.compat.overlay.json" % stem),
            overlaymod.document(
                "Zenesis legacy compatibility - %s - shrink this to zero" % stem, compat
            ),
        )
        note("  %-46s live=%-5d compat=%d" % (path.name, len(live), len(compat)))
    return 0


def cmd_verify(args):
    """
    Prove the conversion is lossless: converted + live + compat == original.

    Any difference means the converter silently changed something the overlays
    do not account for, which is the one failure mode worth blocking a release.
    The `$ref` rewrite is left out here on purpose: it is a prefix swap with an
    exact inverse, covered by the unit tests, and the overlays describe the
    vendor-key separation only.
    """
    config = load_rules(args)
    overlays = pathlib.Path(args.overlays) if args.overlays else None
    failures = 0

    for path in collect(args.source):
        original = read_json(path)
        converted, report = convert(original, config, label=path.name, rewrite_refs=False)

        if overlays and overlays.is_dir():
            live_doc = read_json(overlays / ("%s.live.overlay.json" % path.stem))
            compat_doc = read_json(overlays / ("%s.compat.overlay.json" % path.stem))
            stale = "committed"
        else:
            live, compat = overlaymod.derive(original, converted, LIVE_KEYS)
            live_doc = overlaymod.document("live", live)
            compat_doc = overlaymod.document("compat", compat)
            stale = "derived"

        overlaymod.apply(converted, live_doc)
        overlaymod.apply(converted, compat_doc)

        if converted == original:
            note("  %-46s OK   round trip lossless (%s overlays)" % (path.name, stale))
        else:
            note("  %-46s FAIL round trip lost data" % path.name)
            failures += 1

        if report.warnings and not args.allow_warnings:
            note("  %-46s FAIL %d conversion warning(s)"
                 % ("", len(report.warnings)))
            for where, message in report.warnings:
                note("        * %s" % message)
                note("            at %s" % where)
            failures += 1

    if failures:
        note("")
        note("VERIFY FAILED (%d problem(s))." % failures)
        return 1
    note("")
    note("VERIFY PASSED.")
    return 0


# -------------------------------------------------------------------- main

def build_parser():
    parser = argparse.ArgumentParser(
        prog="zenesis-oas",
        description="Convert between Zenesis-flavoured and clean OpenAPI 3.x, "
                    "in either direction, and compare the two.",
    )
    parser.add_argument("--rules", metavar="FILE",
                        help="rules.json (default: ./rules.json if present, else built-in)")
    sub = parser.add_subparsers(dest="command", required=True)

    zenesis = ("the Zenesis-flavoured side: a .json spec or a directory of them, "
               "e.g. v2.0/zenesis-oas/ or its common/")
    analytics = ("the clean, vendor-neutral side: a .json spec or a directory of them, "
                 "e.g. analytics-oas/v2.0/ or its common/")

    p = sub.add_parser("inventory", help="list vendor extensions without converting")
    p.add_argument("source", metavar="ZENESIS", help=zenesis)
    p.set_defaults(func=cmd_inventory)

    for name in ("to-analytics", "convert"):
        p = sub.add_parser(
            name,
            help="ZENESIS -> ANALYTICS: write clean OpenAPI"
                 + ("" if name == "to-analytics" else " (alias of to-analytics)"),
            description="Read the Zenesis source and write clean, vendor-neutral OpenAPI. "
                        "ANALYTICS is written, never read.",
        )
        p.add_argument("source", metavar="ZENESIS", help=zenesis + " -- read")
        p.add_argument("dest", metavar="ANALYTICS", help=analytics + " -- written")
        p.add_argument("--indent", type=int, default=2)
        p.add_argument("--quiet", action="store_true")
        p.set_defaults(func=cmd_to_analytics)

    p = sub.add_parser(
        "to-zenesis",
        help="ANALYTICS -> ZENESIS: carry edits made in the clean OpenAPI back into the source",
        description="Read the edits made to the clean OpenAPI and write them into the Zenesis "
                    "source. Both paths are read: ANALYTICS supplies the edits, ZENESIS is the "
                    "base of the merge and, with --in-place, is also what gets written.",
        epilog="example:  zenesis-oas to-zenesis ../analytics-oas/v2.0 "
               "v2.0/zenesis-oas --in-place",
    )
    p.add_argument("published", metavar="ANALYTICS",
                   help=analytics + " -- read, for the edits it carries")
    p.add_argument("source", metavar="ZENESIS",
                   help=zenesis + " -- read as the merge base, and written with --in-place")
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument("--in-place", action="store_true",
                       help="write the merged result over ZENESIS")
    where.add_argument("--out", metavar="PATH",
                       help="write the merged result here instead, leaving ZENESIS untouched")
    p.set_defaults(func=cmd_to_zenesis)

    p = sub.add_parser(
        "compare",
        help="ZENESIS vs ANALYTICS: list what differs; writes nothing",
        description="Convert ZENESIS and list every path where ANALYTICS differs from the result. "
                    "Neither path is written.",
    )
    p.add_argument("source", metavar="ZENESIS", help=zenesis + " -- read")
    p.add_argument("published", metavar="ANALYTICS", help=analytics + " -- read")
    p.add_argument("--json", action="store_true", help="machine-readable output on stdout")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("overlay", help="regenerate the Overlay 1.0.0 documents")
    p.add_argument("source", metavar="ZENESIS", help=zenesis)
    p.add_argument("dest", nargs="?", help="unused; accepted for symmetry")
    p.add_argument("--out", default="overlays")
    p.set_defaults(func=cmd_overlay)

    p = sub.add_parser("verify", help="prove the conversion loses nothing")
    p.add_argument("source", metavar="ZENESIS", help=zenesis)
    p.add_argument("dest", nargs="?", help="unused; accepted for symmetry")
    p.add_argument("--overlays", help="directory of committed overlays to check against")
    p.add_argument("--allow-warnings", action="store_true",
                   help="do not fail on conversion warnings")
    p.set_defaults(func=cmd_verify)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as error:
        note("error: %s" % error)
        return 2
    except ValueError as error:
        note("error: %s" % error)
        return 2


if __name__ == "__main__":
    sys.exit(main())
