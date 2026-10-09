"""
Seed component schemas with a worked example taken from their call site.

A Zenesis spec keeps its examples on the Operation Object -- under a media
type, or beside a query parameter -- while the shape they illustrate lives in
`components/schemas`. Anything that renders a schema on its own (Swagger UI's
Schemas panel, `openapi-generator` model docs, an MCP tool description) shows
the referenced schema with no sample value at all, even though the document
contains one a few lines away.

This pass copies the first example of each operation down the `$ref` chain, so
`UpdateRowsConfig` carries the `{"columns": ..., "criteria": ...}` object the
`updateRows` request body demonstrates. It only ever fills a gap: a schema that
already has `example`/`examples` is left exactly as the author wrote it, and a
call site with no example adds nothing -- the key is omitted rather than
written as an empty list.

"First" means first in document order: paths, then operations, then request
body before responses. Two operations sharing a schema therefore give a stable
result across runs, and the winner is the one a reader meets first.
"""

from .jsonpath import escape
from .rules import resolve_pointer

HTTP_METHODS = {
    "get", "put", "post", "delete", "options", "head", "patch", "trace",
}

_MISSING = object()


def propagate(doc, report):
    """Fill empty component schemas with an example from their first call site."""
    paths = doc.get("paths")
    if not isinstance(paths, dict):
        return

    for url, item in paths.items():
        if not isinstance(item, dict):
            continue
        base = "$" + escape("paths") + escape(url)

        _seed_parameters(item.get("parameters"), base, doc, report)

        for method, operation in item.items():
            if method not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            where = base + escape(method)

            _seed_parameters(operation.get("parameters"), where, doc, report)

            body = _deref(operation.get("requestBody"), doc)
            if isinstance(body, dict):
                _seed_content(body.get("content"), where + escape("requestBody"),
                              doc, report)

            responses = operation.get("responses")
            if not isinstance(responses, dict):
                continue
            for code, response in responses.items():
                response = _deref(response, doc)
                if isinstance(response, dict):
                    _seed_content(
                        response.get("content"),
                        where + escape("responses") + escape(code),
                        doc, report,
                    )


# ------------------------------------------------------------- call sites

def _deref(node, doc):
    """
    Follow a local `$ref` one hop, so a shared Parameter or Response Object is
    read at its definition. A `$ref` that leaves this document resolves to
    nothing, which is the correct answer here: the example would have to be
    written into a file we do not own.
    """
    if isinstance(node, dict) and isinstance(node.get("$ref"), str):
        return resolve_pointer(node["$ref"], doc)
    return node


def _seed_parameters(parameters, where, doc, report):
    """A Parameter Object carries its schema and its examples side by side."""
    if not isinstance(parameters, list):
        return
    for index, parameter in enumerate(parameters):
        resolved = _deref(parameter, doc)
        if isinstance(resolved, dict):
            _seed(resolved, "%s%s[%d]" % (where, escape("parameters"), index),
                  doc, report)


def _seed_content(content, where, doc, report):
    if not isinstance(content, dict):
        return
    for media_type, media in content.items():
        if isinstance(media, dict):
            _seed(media, where + escape("content") + escape(media_type),
                  doc, report)


def _seed(node, where, doc, report):
    """Push `node`'s first example down whatever its `schema` refers to."""
    schema = node.get("schema")
    if not isinstance(schema, dict):
        return
    value = _first_example(node, doc)
    if value is _MISSING:
        return
    _distribute(schema, value, doc, report, frozenset())


def _first_example(node, doc):
    """
    The first sample value a Media Type or Parameter Object offers.

    The `examples` map is checked before the singular `example` because that is
    what the Zenesis specs use; both are legal in the same position.
    """
    examples = node.get("examples")
    if isinstance(examples, dict):
        for example in examples.values():
            example = _deref(example, doc)
            if isinstance(example, dict) and "value" in example:
                return example["value"]
    if "example" in node:
        return node["example"]
    return _MISSING


# ------------------------------------------------------------ distribution

def _distribute(schema, value, doc, report, seen):
    """
    Walk `schema` and `value` together, attaching each fragment to the
    component schema that describes it.

    `seen` holds the $refs already on this branch, so a schema that refers to
    itself terminates instead of recursing forever.
    """
    if not isinstance(schema, dict):
        return

    ref = schema.get("$ref")
    if isinstance(ref, str):
        # External $refs point outside this document; there is nothing local
        # to write to, and nothing to descend into.
        if ref in seen or not ref.startswith("#/"):
            return
        target = resolve_pointer(ref, doc)
        if not isinstance(target, dict):
            return
        _attach(target, value, report)
        _distribute(target, value, doc, report, seen | {ref})
        return

    # An inline schema sits next to the example already, so it is a route to
    # the components below it rather than somewhere to write.
    properties = schema.get("properties")
    if isinstance(properties, dict) and isinstance(value, dict):
        for name, sub in properties.items():
            if name in value:
                _distribute(sub, value[name], doc, report, seen)

    items = schema.get("items")
    if isinstance(items, dict) and isinstance(value, list) and value:
        _distribute(items, value[0], doc, report, seen)

    # allOf composes one shape, so the whole value describes every branch.
    # oneOf/anyOf choose between shapes, and picking the wrong branch would
    # document an example that does not validate -- so they are left alone.
    composed = schema.get("allOf")
    if isinstance(composed, list):
        for sub in composed:
            _distribute(sub, value, doc, report, seen)


def _attach(schema, value, report):
    if "examples" in schema or "example" in schema:
        report.hit("schema example already authored, left as written")
        return
    if value is None:
        return
    schema["examples"] = [value]
    report.hit("schema examples seeded from its first call site")
