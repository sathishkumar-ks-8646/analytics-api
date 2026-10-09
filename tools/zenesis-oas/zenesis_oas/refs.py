"""
Repoint `$ref`s that leave the document.

Every specification references the shared components file by absolute URL.
In the source repository that URL is the raw-file address of
`vN.N/zenesis-oas/common/zoho-analytics-api-common.json` in this repository; in the
published repository it is the same file's address under zoho/analytics-oas.
The converter swaps one for the other on the way out, and the reverse
direction swaps them back. Both are configured under `common_ref` in
rules.json; when it is absent nothing is rewritten.
"""


def rewrite(doc, old, new):
    """
    Replace the prefix `old` with `new` in every `$ref` string under `doc`,
    in place. Returns how many were changed. A `$ref` is
    `<file-url>#<pointer>`, so matching on the prefix leaves the pointer alone.
    """
    if not old or not new or old == new:
        return 0
    count = 0

    def walk(node):
        nonlocal count
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str) and value.startswith(old):
                    node[key] = new + value[len(old):]
                    count += 1
                else:
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(doc)
    return count


def endpoints(config):
    """(source_url, published_url) from the config, or None when unset."""
    common = (config or {}).get("common_ref")
    if not isinstance(common, dict):
        return None
    source, published = common.get("source"), common.get("published")
    if not (isinstance(source, str) and isinstance(published, str)):
        return None
    if source == published:
        return None
    return source, published


def to_published(doc, config, report=None):
    pair = endpoints(config)
    if pair is None:
        return 0
    count = rewrite(doc, pair[0], pair[1])
    if report is not None and count:
        report.hit("$ref to the common file repointed at the published URL", count)
    return count


def to_source(doc, config, report=None):
    pair = endpoints(config)
    if pair is None:
        return 0
    count = rewrite(doc, pair[1], pair[0])
    if report is not None and count:
        report.hit("$ref to the common file repointed at the source URL", count)
    return count
