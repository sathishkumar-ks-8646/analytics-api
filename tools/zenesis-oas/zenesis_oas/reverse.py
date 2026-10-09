"""
The other direction: carry edits made to a published, vendor-neutral document
back into the Zenesis source it was converted from.

A clean document cannot simply be "converted back" -- the renderer-only
content (`x-zenesis-sections`, `x-zenesis-statuscodes`, `x-zenesis-security`,
`x-zenesis-doc`, ...) is not in it, and the Markdown the converter folded into
descriptions does not round-trip to the HTML it came from. So this is a
three-way merge rather than an inverse function:

    base      the Zenesis source as it stands
    expected  convert(base) -- what the published document *should* look like
    actual    the published document as someone edited it

Wherever `actual` differs from `expected`, that difference is an edit, and it
is written onto `base` at the same location. Four places need translation on
the way: `x-enumDescriptions` becomes the positional `x-zenesis-enums-desc`
again, an Example Object's `summary`/`description` are swapped back for the
renderer, a `$ref` to the published common file is repointed at the source
file, and an edit to an operation description is accepted only above the
folded Notes / Error codes / Rate limit blocks. Anything that cannot be
carried is reported as a warning and left alone, never guessed at.

`compare()` is the read-only half: it lists the differences without applying
them, which is also how `to-zenesis` proves afterwards that nothing remains.
"""

import copy

from . import refs
from .converter import convert, _child_kind
from .jsonpath import escape, find, parse
from .report import Report
from .rules import load_rules

ENUM_KEYS = ("enum", "x-enumDescriptions", "x-enum-varnames")


class ReverseContext:
    def __init__(self, config):
        self.config = config
        self.options = config.get("options", {})
        # Edits to content the converter derives (seeded schema examples). They
        # are judged after the merge: if re-converting the merged source
        # reproduces the edit, the origin was edited too and nothing is lost.
        self.deferred = []


# ----------------------------------------------------------------- compare

def compare(expected, actual, path="$"):
    """
    Yield (path, kind, expected_value, actual_value) for every difference.

    kind is "changed", "only-in-source" (present in the conversion of the
    source but not in the published document) or "only-in-published".
    Lists of different length are reported once, at the list, rather than
    element by element -- the alignment below the change is a guess.
    """
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected:
            if key not in actual:
                yield path + escape(key), "only-in-source", expected[key], None
            else:
                yield from compare(expected[key], actual[key], path + escape(key))
        for key in actual:
            if key not in expected:
                yield path + escape(key), "only-in-published", None, actual[key]
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            yield path, "changed", expected, actual
        else:
            for index, (e, a) in enumerate(zip(expected, actual)):
                yield from compare(e, a, "%s[%d]" % (path, index))
    elif expected != actual:
        yield path, "changed", expected, actual


# ----------------------------------------------------------------- reverse

def reverse(actual, base, config=None, label=None):
    """
    Merge the edits in `actual` (a published document) onto `base` (its
    Zenesis source). Returns (merged_source, Report). Neither input is
    modified.
    """
    config = config or load_rules()
    report = Report(label)

    expected, conversion = convert(base, config, label=label)
    for where, message in conversion.warnings:
        report.warn(where, "converting the source gave a warning, so the "
                           "comparison baseline may be off: " + message)

    merged = copy.deepcopy(base)
    ctx = ReverseContext(config)
    _merge(merged, expected, actual, "$", ctx, report, kind="root", parent_key=None)

    if ctx.deferred:
        again, _ = convert(merged, config, label=label)
        for where, message in ctx.deferred:
            segments = parse(where)
            now = [m[2] for m in find(again, segments)]
            wanted = [m[2] for m in find(actual, segments)]
            if now and now == wanted:
                report.hit("derived content caught up with its edited origin")
            else:
                report.warn(where, message)
    return merged, report


def _same_shape(base, expected, actual):
    if isinstance(expected, dict) and isinstance(actual, dict) and isinstance(base, dict):
        return True
    if (isinstance(expected, list) and isinstance(actual, list) and isinstance(base, list)
            and len(expected) == len(actual) == len(base)):
        return True
    return False


EXAMPLE_FIELDS = ("summary", "description")


def _merge(base, expected, actual, path, ctx, report, kind, parent_key, skip=()):
    """Walk the three documents together; `base` is edited in place."""
    if isinstance(base, dict):
        handled = set(skip)
        swapped_examples = set()

        if any(expected.get(k) != actual.get(k) for k in ENUM_KEYS) and (
                "enum" in expected or "enum" in actual):
            _merge_enum(base, expected, actual, path, report)
            handled.update(ENUM_KEYS)

        # This is an `examples` map: the converter swapped the two text fields
        # on each Example Object below it, so write those two back through the
        # same swap and let the generic walk handle the rest of each example.
        if parent_key == "examples" and ctx.options.get("unswap_examples", True):
            for name in expected:
                if not (name in actual and name in base and isinstance(base[name], dict)
                        and isinstance(expected[name], dict) and isinstance(actual[name], dict)):
                    continue
                if any(expected[name].get(f) != actual[name].get(f) for f in EXAMPLE_FIELDS):
                    _merge_example(base[name], expected[name], actual[name],
                                   path + escape(name), report)
                    swapped_examples.add(name)

        if kind == "operation" and expected.get("description") != actual.get("description"):
            _merge_description(base, expected, actual, path, report)
            handled.add("description")

        keys = list(expected) + [k for k in actual if k not in expected]
        for key in keys:
            if key in handled:
                continue
            here = path + escape(key)
            in_expected, in_actual = key in expected, key in actual

            if in_expected and not in_actual:
                if key in base:
                    del base[key]
                    report.hit("key removed from the source")
                else:
                    report.warn(here, "removed in the published document, but the "
                                      "converter derived it (it is not in the source); "
                                      "nothing to remove")
                continue

            if in_actual and not in_expected:
                if key in base:
                    report.warn(here, "added in the published document, but the source "
                                      "already has a key of that name which the converter "
                                      "removes; left as it was")
                else:
                    base[key] = _translate(actual[key], ctx, key)
                    report.hit("key added to the source")
                continue

            if expected[key] == actual[key]:
                continue
            if key not in base:
                ctx.deferred.append((here, "edited in the published document, but this "
                                           "content is derived by the converter (for example "
                                           "a schema example seeded from its call site) and "
                                           "the edit is not reproduced by what it derives "
                                           "from; edit the origin instead"))
                continue

            if _same_shape(base[key], expected[key], actual[key]):
                _merge(base[key], expected[key], actual[key], here, ctx, report,
                       _child_kind(kind, key), key,
                       skip=EXAMPLE_FIELDS if key in swapped_examples else ())
            else:
                base[key] = _translate(actual[key], ctx, key)
                report.hit("value replaced in the source")

    elif isinstance(base, list):
        for index, (b, e, a) in enumerate(zip(base, expected, actual)):
            if e == a:
                continue
            here = "%s[%d]" % (path, index)
            if _same_shape(b, e, a):
                _merge(b, e, a, here, ctx, report, "other", parent_key)
            else:
                base[index] = _translate(a, ctx, parent_key)
                report.hit("value replaced in the source")


def _merge_enum(base, expected, actual, path, report):
    """
    `x-enumDescriptions` is keyed by value; `x-zenesis-enums-desc` is a
    positional array parallel to `enum`. Rebuild the array from the map in
    the order of the (possibly edited) enum. `x-enum-varnames` is derived
    from the labels and is never written back.
    """
    values = actual.get("enum")
    if not isinstance(values, list):
        base.pop("enum", None)
        base.pop("x-zenesis-enums-desc", None)
        report.hit("enum removed from the source")
        return

    base["enum"] = copy.deepcopy(values)
    labels = actual.get("x-enumDescriptions")

    if isinstance(labels, dict):
        missing = [v for v in values if str(v) not in labels]
        if missing:
            report.warn(path, "x-enumDescriptions has no label for %s; "
                              "x-zenesis-enums-desc not rebuilt because a positional "
                              "array cannot have gaps" % ", ".join(repr(v) for v in missing))
        else:
            base["x-zenesis-enums-desc"] = [str(labels[str(v)]) for v in values]
            report.hit("x-zenesis-enums-desc rebuilt from x-enumDescriptions")
        extra = [k for k in labels if k not in {str(v) for v in values}]
        if extra:
            report.warn(path, "x-enumDescriptions labels %s have no enum value and "
                              "were dropped" % ", ".join(repr(k) for k in extra))
    elif "x-enumDescriptions" in expected:
        base.pop("x-zenesis-enums-desc", None)
        report.hit("x-zenesis-enums-desc removed from the source")
    elif "x-zenesis-enums-desc" in base and len(base["x-zenesis-enums-desc"]) != len(values):
        report.warn(path, "enum now has %d values but the source has %d labels in "
                          "x-zenesis-enums-desc; add x-enumDescriptions to the published "
                          "document so the labels can be rebuilt"
                    % (len(values), len(base["x-zenesis-enums-desc"])))

    if (actual.get("x-enum-varnames") != expected.get("x-enum-varnames")
            and labels == expected.get("x-enumDescriptions")):
        report.warn(path, "x-enum-varnames was edited; it is derived from the labels, "
                          "so the edit is not carried -- change x-enumDescriptions")


def _merge_example(base, expected, actual, path, report):
    """
    The converter swapped `summary` and `description` on this Example Object
    if the source had them the Zenesis way round (long text in `summary`).
    Write the edits back through the same swap.
    """
    swapped = (
        base.get("summary") == expected.get("description")
        and base.get("description") == expected.get("summary")
        and base.get("summary") != base.get("description")
    )
    pairs = (("summary", "description"), ("description", "summary")) if swapped else (
        ("summary", "summary"), ("description", "description"))
    for published_key, source_key in pairs:
        if published_key in actual:
            base[source_key] = actual[published_key]
        else:
            base.pop(source_key, None)
    report.hit("example label/prose written back%s" % (" (re-swapped)" if swapped else ""))


def _merge_description(base, expected, actual, path, report):
    """
    The published description is the source description plus whatever the
    converter folded in (Notes, Error codes, Rate limit). Accept an edit to
    the part that came from the source; refuse one that touches the folded
    tail, because that text lives in the vendor keys and would be lost on the
    next conversion.
    """
    source = (base.get("description") or "").strip()
    published = expected.get("description") or ""
    edited = actual.get("description")

    if edited is None:
        report.warn(path + escape("description"),
                    "removed in the published document; the source description and "
                    "the notes folded into it are left in place")
        return

    if not published.startswith(source):
        report.warn(path + escape("description"),
                    "cannot tell the source text from the folded notes; left unchanged")
        return

    tail = published[len(source):]
    if tail and not edited.endswith(tail):
        report.warn(path + escape("description"),
                    "the edit touches text the converter folded in from "
                    "x-zenesis-sections / x-zenesis-statuscodes / x-zenesis-security; "
                    "edit those keys in the source instead. Left unchanged")
        return

    head = edited[: len(edited) - len(tail)] if tail else edited
    head = head.rstrip()
    if head:
        base["description"] = head
    else:
        base.pop("description", None)
    report.hit("operation description edited above the folded notes")


def _translate(value, ctx, parent_key=None):
    """
    Convert a fragment that exists only in the published document into
    source conventions, recursively: `$ref`s repointed, `x-enumDescriptions`
    rebuilt as `x-zenesis-enums-desc`, `x-enum-varnames` dropped, and Example
    Objects swapped back.
    """
    value = copy.deepcopy(value)
    refs.to_source(value, ctx.config)
    return _translate_inner(value, ctx, parent_key)


def _translate_inner(value, ctx, parent_key):
    if isinstance(value, dict):
        if isinstance(value.get("enum"), list) and isinstance(value.get("x-enumDescriptions"), dict):
            labels = value.pop("x-enumDescriptions")
            if all(str(v) in labels for v in value["enum"]):
                value["x-zenesis-enums-desc"] = [str(labels[str(v)]) for v in value["enum"]]
        value.pop("x-enum-varnames", None)

        if parent_key == "examples" and ctx.options.get("unswap_examples", True):
            for name, example in value.items():
                if (isinstance(example, dict)
                        and isinstance(example.get("summary"), str)
                        and isinstance(example.get("description"), str)
                        and len(example["description"]) > len(example["summary"])):
                    example["summary"], example["description"] = (
                        example["description"], example["summary"])

        for key, child in list(value.items()):
            value[key] = _translate_inner(child, ctx, key)
        return value
    if isinstance(value, list):
        return [_translate_inner(v, ctx, parent_key) for v in value]
    return value
