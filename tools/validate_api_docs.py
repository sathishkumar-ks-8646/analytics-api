#!/usr/bin/env python3
"""Validate the Zoho Analytics API source documents, every version of them.

The repository holds one directory per API version, named by the version
index at the root:

    manifest.json                  which vN.N directories exist, which is latest
    vN.N/manifest.json             that version's inventory: domains, API groups,
                                   and the URL its specs use for the common file
    vN.N/md/                       narrative reference, one folder per domain
    vN.N/zenesis-oas/              OpenAPI with x-zenesis-* extensions, one per domain
    vN.N/zenesis-oas/common/       the components every specification shares
    vN.N/zenesis-oas-samples/      SDK snippets, one per domain

For each version this checks the three things a consumer depends on: naming
(folders and files follow the export convention), completeness (every domain
has markdown, a spec and samples, and every documented group exists in both)
and integrity (the JSON parses, samples point at real operations, every remote
$ref targets this version's common file, and no unknown vendor extension has
appeared). It also checks the version index itself.

Standard library only, Python 3.8+. Run from anywhere:

    python3 tools/validate_api_docs.py                 every version
    python3 tools/validate_api_docs.py --version v2.0  one version

Exits 0 when errors=0. Warnings never fail the run on their own; pass
--strict to fail on them too.
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_MANIFEST = os.path.join(ROOT, 'manifest.json')

COMMON_NAME = 'zoho-analytics-api-common.json'
HTTP_METHODS = ('get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace')

VERSION_DIR_RE = re.compile(r'^v\d+\.\d+$')
VERSION_STATUSES = ('draft', 'current', 'deprecated')
MD_STEM_RE = re.compile(r'^[A-Z0-9]+(?:_[A-Z0-9]+)*$')
MD_FOLDER_RE = re.compile(r'^(\d{2}) · (.+)$')

# What may sit beside the version directories, and what may sit inside one.
# Anything else is reported: this repository holds the API documents and what is built from them.
ROOT_ALLOWED = {
    'tools', '.git', '.github', 'manifest.json', 'README.md', 'CHANGELOG.md',
    'LICENSE.md', 'CLAUDE.md', 'AGENTS.md', 'Makefile', '.gitignore', 'dist',
}
# A version directory holds the authored sources (md, zenesis-oas, zenesis-oas-samples)
# and the artefacts built from them (oas, okf, postman). Only the sources are checked here;
# the generated directories have validators of their own under tools/.
VERSION_ALLOWED = {
    'md', 'zenesis-oas', 'zenesis-oas-samples', 'manifest.json', 'README.md',
    'oas', 'okf', 'postman',
}
# The shared components file sits with the documents that reference it.
COMMON_SUBDIR = 'common'

# Vendor extensions the converter knows how to handle. Keep in step with
# `tools/zenesis-oas/rules.json`: a key that appears here but not there
# is dropped silently by the converter, and the reverse is dead configuration.
KNOWN_VENDOR_KEYS = {
    'x-zenesis-title',
    'x-zenesis-doc',
    'x-zenesis-usecase-tag',
    'x-zenesis-sections',
    'x-zenesis-enums-desc',
    'x-zenesis-statuscodes',
    'x-zenesis-security',
    'x-zenesis-shared-note',
    'x-zenesis-shared-notes',
    'x-zenesis-description-pageName',
}

# The error-response model. Every operation carries one success response and
# these two error responses, each a $ref into the shared common file.
SUCCESS_CODES = ('200', '201', '204')
ERROR_CODES = {
    '4XX': '#/components/responses/CommonErrorResponse',
    '500': '#/components/responses/UnexpectedErrorResponse',
}

errors = []
warnings = []


def error(msg):
    errors.append(msg)
    print('ERROR ' + msg)


def warn(msg):
    warnings.append(msg)
    print('WARN  ' + msg)


def rel(path):
    return os.path.relpath(path, ROOT)


def load_json(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        error('%s: invalid JSON: %s' % (rel(path), exc))
    except OSError as exc:
        error('%s: cannot read: %s' % (rel(path), exc))
    return None


def walk_keys(node, found):
    """Collect every `x-` key anywhere in the document."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key.startswith('x-'):
                found.add(key)
            walk_keys(value, found)
    elif isinstance(node, list):
        for value in node:
            walk_keys(value, found)


def walk_refs(node, found):
    """Collect every `$ref` value anywhere in the document."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == '$ref' and isinstance(value, str):
                found.append(value)
            walk_refs(value, found)
    elif isinstance(node, list):
        for value in node:
            walk_refs(value, found)


# ------------------------------------------------------------ version index

class Version:
    """One vN.N directory: its paths and the inventory from its manifest."""

    def __init__(self, name, entry):
        self.name = name
        self.entry = entry
        self.dir = os.path.join(ROOT, name)
        self.manifest_file = os.path.join(self.dir, 'manifest.json')
        self.md_dir = os.path.join(self.dir, 'md')
        self.oas_dir = os.path.join(self.dir, 'zenesis-oas')
        self.samples_dir = os.path.join(self.dir, 'zenesis-oas-samples')
        self.common_dir = os.path.join(self.oas_dir, COMMON_SUBDIR)
        self.common_file = os.path.join(self.common_dir, COMMON_NAME)
        # [(markdown folder, OpenAPI file stem, [(markdown stem, OpenAPI tag), ...])]
        self.domains = []
        self.common_ref = None


def check_index():
    """The root manifest names every version directory, and vice versa."""
    on_disk = sorted(d for d in os.listdir(ROOT)
                     if VERSION_DIR_RE.match(d) and os.path.isdir(os.path.join(ROOT, d)))

    if not os.path.isfile(ROOT_MANIFEST):
        error('manifest.json: missing; it is the version index every consumer '
              'starts from')
        return [Version(d, {}) for d in on_disk]
    index = load_json(ROOT_MANIFEST)
    if not isinstance(index, dict):
        return []

    entries = index.get('versions')
    if not isinstance(entries, list) or not entries:
        error('manifest.json: "versions" must be a non-empty list')
        return []

    versions, listed = [], []
    for entry in entries:
        if not isinstance(entry, dict):
            error('manifest.json: every entry in "versions" must be an object')
            continue
        name = entry.get('version')
        if not isinstance(name, str) or not VERSION_DIR_RE.match(name):
            error('manifest.json: version %r must look like "v2.0"' % (name,))
            continue
        if name in listed:
            error('manifest.json: version %s is listed twice' % name)
            continue
        listed.append(name)
        if entry.get('path') != name:
            error('manifest.json: %s has path %r; the directory is named after '
                  'the version' % (name, entry.get('path')))
        if entry.get('manifest') != name + '/manifest.json':
            error('manifest.json: %s must point at "%s/manifest.json"'
                  % (name, name))
        if entry.get('status') not in VERSION_STATUSES:
            error('manifest.json: %s has status %r; expected one of %s'
                  % (name, entry.get('status'), ', '.join(VERSION_STATUSES)))
        if not os.path.isdir(os.path.join(ROOT, name)):
            error('manifest.json: %s is listed but the directory does not exist'
                  % name)
            continue
        versions.append(Version(name, entry))

    for name in on_disk:
        if name not in listed:
            error('%s/: version directory is not listed in manifest.json' % name)

    current = [v.name for v in versions if v.entry.get('status') == 'current']
    if len(current) != 1:
        error('manifest.json: exactly one version must have status "current", '
              'found %s' % (current or 'none'))
    latest = index.get('latest')
    if latest not in listed:
        error('manifest.json: "latest" is %r, which is not a listed version'
              % (latest,))
    elif current and latest != current[0]:
        warn('manifest.json: "latest" is %s but the current version is %s'
             % (latest, current[0]))

    for name in sorted(os.listdir(ROOT)):
        if name in ROOT_ALLOWED or name in listed or name.startswith('.'):
            continue
        warn('%s: unexpected entry at the repository root; versions live in '
             'vN.N/ directories listed in manifest.json' % name)

    return versions


def load_version_manifest(version):
    """Read vN.N/manifest.json into the Version. False when unusable."""
    if not os.path.isfile(version.manifest_file):
        error('%s/manifest.json: missing; it lists the domains and groups of '
              'this version' % version.name)
        return False
    manifest = load_json(version.manifest_file)
    if not isinstance(manifest, dict):
        return False

    if manifest.get('version') != version.name:
        error('%s/manifest.json: "version" is %r; it must match the directory '
              'name' % (version.name, manifest.get('version')))
    for key in ('api_version', 'title', 'status'):
        if not manifest.get(key):
            error('%s/manifest.json: "%s" is required' % (version.name, key))
    if version.entry.get('status') and manifest.get('status') != version.entry.get('status'):
        error('%s/manifest.json: status %r disagrees with manifest.json (%r)'
              % (version.name, manifest.get('status'), version.entry.get('status')))

    ref = manifest.get('common_ref')
    tail = '/%s/zenesis-oas/%s/%s' % (version.name, COMMON_SUBDIR, COMMON_NAME)
    if (not isinstance(ref, str) or not ref.startswith('https://')
            or not ref.endswith(tail)):
        error('%s/manifest.json: "common_ref" must be the https URL ending in '
              '%s; every remote $ref in the specs targets it'
              % (version.name, tail))
    else:
        version.common_ref = ref

    domains = manifest.get('domains')
    if not isinstance(domains, list) or not domains:
        error('%s/manifest.json: "domains" must be a non-empty list'
              % version.name)
        return False

    slugs, folders = set(), set()
    for domain in domains:
        folder, slug, groups = (domain.get('folder'), domain.get('slug'),
                                domain.get('groups'))
        if not isinstance(folder, str) or not isinstance(slug, str):
            error('%s/manifest.json: every domain needs a "folder" and a "slug"'
                  % version.name)
            continue
        if slug in slugs:
            error('%s/manifest.json: slug %r is used by two domains'
                  % (version.name, slug))
        if folder in folders:
            error('%s/manifest.json: folder %r is used by two domains'
                  % (version.name, folder))
        slugs.add(slug)
        folders.add(folder)
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
            error('%s/manifest.json: slug %r must be lower-case words joined '
                  'by hyphens' % (version.name, slug))
        pairs = []
        if not isinstance(groups, list) or not groups:
            error('%s/manifest.json: domain %r has no groups'
                  % (version.name, slug))
        else:
            for group in groups:
                stem, tag = group.get('md'), group.get('tag')
                if not isinstance(stem, str) or not isinstance(tag, str):
                    error('%s/manifest.json: every group in %r needs "md" and '
                          '"tag"' % (version.name, slug))
                    continue
                pairs.append((stem, tag))
        version.domains.append((folder, slug, pairs))
    return True


# --------------------------------------------------------------- per version

def check_layout(version):
    for name, path in (('md', version.md_dir), ('zenesis-oas', version.oas_dir),
                       ('zenesis-oas-samples', version.samples_dir)):
        if not os.path.isdir(path):
            error('%s/%s/: missing required directory' % (version.name, name))
    if not os.path.isfile(version.common_file):
        error('%s: missing' % rel(version.common_file))

    for name in sorted(os.listdir(version.dir)):
        if name not in VERSION_ALLOWED and not name.startswith('.'):
            warn('%s/%s: unexpected entry in a version directory' % (version.name, name))
    if os.path.isdir(version.common_dir):
        for name in sorted(os.listdir(version.common_dir)):
            if name not in (COMMON_NAME, 'README.md') and not name.startswith('.'):
                warn('%s/%s: unexpected entry; only the shared components file '
                     'belongs here' % (rel(version.common_dir), name))


def check_markdown(version):
    """Folder and file naming, and one markdown file per documented group."""
    if not os.path.isdir(version.md_dir):
        return
    present = sorted(d for d in os.listdir(version.md_dir)
                     if os.path.isdir(os.path.join(version.md_dir, d)))
    expected = [d[0] for d in version.domains]

    for folder in present:
        where = '%s/md/%s' % (version.name, folder)
        if not MD_FOLDER_RE.match(folder):
            error('%s: folder name must be "NN · Title" with a middle dot '
                  '(U+00B7)' % where)
        if folder not in expected:
            error('%s: folder is not listed in %s/manifest.json'
                  % (where, version.name))

    for index, (folder, _slug, groups) in enumerate(version.domains, start=1):
        path = os.path.join(version.md_dir, folder)
        where = '%s/md/%s' % (version.name, folder)
        if not os.path.isdir(path):
            error('%s: listed in %s/manifest.json but not present'
                  % (where, version.name))
            continue
        if not folder.startswith('%02d · ' % index):
            error('%s: expected prefix "%02d · "; domain folders are numbered '
                  'consecutively from 01 in manifest order' % (where, index))

        files = sorted(f for f in os.listdir(path) if not f.startswith('.'))
        for name in files:
            if not name.endswith('.md'):
                error('%s/%s: only .md files belong here' % (where, name))
                continue
            stem = name[:-3]
            if not MD_STEM_RE.match(stem):
                error('%s/%s: file name must be UPPER_SNAKE_CASE.md' % (where, name))
            if stem not in [g[0] for g in groups]:
                error('%s/%s: group is not listed in %s/manifest.json'
                      % (where, name, version.name))

        for stem, _tag in groups:
            if stem + '.md' not in files:
                error('%s/%s.md: listed in %s/manifest.json but not present'
                      % (where, stem, version.name))
                continue
            check_markdown_body(os.path.join(path, stem + '.md'))


def check_markdown_body(path):
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().splitlines()
    if not lines or not lines[0].startswith('# '):
        error('%s: must open with a single H1 title line' % rel(path))
    if not any(re.match(r'^## \d+\. ', line) for line in lines):
        warn('%s: no "## N. Title" endpoint section found; the OKF builder '
             'joins endpoints on those headings' % rel(path))


def check_specs(version):
    """Every domain has a spec and a samples file, and they agree."""
    expected_specs = {slug + '-grouped-api.json' for _f, slug, _g in version.domains}
    expected_samples = {slug + '-grouped-api-samples.json'
                        for _f, slug, _g in version.domains}

    for directory, expected, suffix in (
            (version.oas_dir, expected_specs, '-grouped-api.json'),
            (version.samples_dir, expected_samples, '-grouped-api-samples.json')):
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.startswith('.') or name == 'README.md':
                continue
            where = '%s/%s' % (rel(directory), name)
            if os.path.isdir(os.path.join(directory, name)):
                # The specifications directory holds one subdirectory, the
                # common components the specifications reference.
                if not (directory == version.oas_dir and name == COMMON_SUBDIR):
                    warn('%s/: unexpected directory' % where)
                continue
            if not name.endswith(suffix):
                error('%s: file name must end with "%s"' % (where, suffix))
            elif name not in expected:
                error('%s: domain is not listed in %s/manifest.json'
                      % (where, version.name))

    total_paths = total_ops = 0
    vendor_keys = set()

    for folder, slug, groups in version.domains:
        spec_path = os.path.join(version.oas_dir, slug + '-grouped-api.json')
        samples_path = os.path.join(version.samples_dir,
                                    slug + '-grouped-api-samples.json')

        if not os.path.isfile(spec_path):
            error('%s: missing (domain "%s")' % (rel(spec_path), folder))
            continue
        if not os.path.isfile(samples_path):
            error('%s: missing (domain "%s")' % (rel(samples_path), folder))

        spec = load_json(spec_path)
        if spec is None:
            continue
        walk_keys(spec, vendor_keys)
        check_remote_refs(version, spec_path, spec)

        if not str(spec.get('openapi', '')).startswith('3.'):
            error('%s: openapi version must be 3.x, found %r'
                  % (rel(spec_path), spec.get('openapi')))
        if 'info' not in spec or 'paths' not in spec:
            error('%s: an OpenAPI document needs "info" and "paths"' % rel(spec_path))
            continue

        declared_tags = [t.get('name') for t in spec.get('tags', [])]
        for _md_stem, tag in groups:
            if tag not in declared_tags:
                error('%s: tag %r is expected by %s/manifest.json but is not '
                      'declared in the document' % (rel(spec_path), tag, version.name))
        for tag in declared_tags:
            if tag not in [g[1] for g in groups]:
                error('%s: tag %r has no markdown group in %s/md/%s; add the '
                      'document and list it in %s/manifest.json'
                      % (rel(spec_path), tag, version.name, folder, version.name))

        operations = {}
        for path, item in spec['paths'].items():
            total_paths += 1
            if not path.startswith('/'):
                error('%s: path %r must start with "/"' % (rel(spec_path), path))
            for method, operation in item.items():
                if method not in HTTP_METHODS:
                    continue
                total_ops += 1
                operations.setdefault(path, set()).add(method)
                title = operation.get('x-zenesis-title') or operation.get('summary')
                if not title:
                    error('%s: %s %s has neither x-zenesis-title nor summary; '
                          'the OKF builder joins endpoints by title'
                          % (rel(spec_path), method.upper(), path))
                elif (operation.get('x-zenesis-title')
                      and operation.get('summary')
                      and operation['x-zenesis-title'].strip()
                      != operation['summary'].strip()):
                    warn('%s: %s %s has x-zenesis-title %r != summary %r; the '
                         'converter drops the title and would lose that text'
                         % (rel(spec_path), method.upper(), path,
                            operation['x-zenesis-title'], operation['summary']))
                for tag in operation.get('tags', []) or []:
                    if tag not in declared_tags:
                        error('%s: %s %s is tagged %r, which the document does '
                              'not declare' % (rel(spec_path), method.upper(),
                                               path, tag))
                if not operation.get('tags'):
                    error('%s: %s %s has no tag, so it belongs to no group'
                          % (rel(spec_path), method.upper(), path))
                check_responses(spec_path, method, path,
                                operation.get('responses', {}))

        samples = load_json(samples_path) if os.path.isfile(samples_path) else None
        if not isinstance(samples, dict):
            if samples is not None:
                error('%s: samples must be an object keyed by path' % rel(samples_path))
            continue
        for path, by_method in samples.items():
            if path not in operations:
                error('%s: samples for %r, which the spec does not define'
                      % (rel(samples_path), path))
                continue
            if not isinstance(by_method, dict):
                error('%s: %r must map a method to its snippets'
                      % (rel(samples_path), path))
                continue
            for method in by_method:
                if method.lower() not in operations[path]:
                    error('%s: samples for %s %s, which the spec does not define'
                          % (rel(samples_path), method.upper(), path))
        for path in operations:
            if path not in samples:
                warn('%s: no SDK samples for %s' % (rel(samples_path), path))

    unknown = sorted(k for k in vendor_keys
                     if k.startswith('x-zenesis-') and k not in KNOWN_VENDOR_KEYS)
    for key in unknown:
        error('%s: %s is used but has no rule in the converter; add it to '
              'tools/zenesis-oas/rules.json and to KNOWN_VENDOR_KEYS here'
              % (version.name, key))
    unused = sorted(KNOWN_VENDOR_KEYS - vendor_keys)
    for key in unused:
        warn('%s: %s is declared known but appears in no spec' % (version.name, key))

    return total_paths, total_ops


def check_remote_refs(version, spec_path, spec):
    """Every remote $ref targets this version's common file, at the URL the
    manifest declares. A $ref into another version, or into the old flat
    layout, would resolve to the wrong components or to nothing."""
    if version.common_ref is None:
        return
    refs = []
    walk_refs(spec, refs)
    seen = set()
    for ref in refs:
        if not ref.startswith(('http://', 'https://')):
            continue
        target = ref.split('#', 1)[0]
        if target != version.common_ref and target not in seen:
            seen.add(target)
            error('%s: remote $ref targets %s; every remote $ref must point at '
                  'the common_ref in %s/manifest.json'
                  % (rel(spec_path), target, version.name))


def check_responses(spec_path, method, path, responses):
    """Every operation models errors the same way: one success response, a
    `4XX` and a `500` that reference the shared error responses, and no
    `default`. The error-code table (`x-zenesis-statuscodes`) rides on the
    success response, which is where the converter and the OKF builder look."""
    where = '%s: %s %s' % (rel(spec_path), method.upper(), path)
    success = [c for c in SUCCESS_CODES if c in responses]
    if len(success) != 1:
        error('%s must have exactly one success response (%s), found %s'
              % (where, '/'.join(SUCCESS_CODES), success or 'none'))
    if 'default' in responses:
        error('%s uses a "default" response; model errors as "4XX" and "500" '
              'like every other operation' % where)
    for code in ERROR_CODES:
        response = responses.get(code)
        if not isinstance(response, dict):
            error('%s is missing the "%s" error response' % (where, code))
        elif not str(response.get('$ref', '')).endswith(ERROR_CODES[code]):
            error('%s: "%s" must $ref the shared %s, found %r'
                  % (where, code, ERROR_CODES[code].split('/')[-1],
                     response.get('$ref')))
    for code, response in responses.items():
        if (isinstance(response, dict) and 'x-zenesis-statuscodes' in response
                and code not in SUCCESS_CODES):
            error('%s: x-zenesis-statuscodes sits on the "%s" response; it '
                  'belongs on the success response' % (where, code))


def check_common(version):
    if not os.path.isfile(version.common_file):
        return
    common = load_json(version.common_file)
    if common is None:
        return
    components = common.get('components')
    if not isinstance(components, dict):
        error('%s: expected a "components" object' % rel(version.common_file))
        return
    schemes = components.get('securitySchemes', {})
    if 'iam-oauth2-schema' not in schemes:
        error('%s: securitySchemes must define "iam-oauth2-schema"; every '
              'operation references it' % rel(version.common_file))
    for pointer in ERROR_CODES.values():
        name = pointer.split('/')[-1]
        if name not in components.get('responses', {}):
            error('%s: responses must define "%s"; every operation references it'
                  % (rel(version.common_file), name))


def check_version(version):
    """Run every per-version check. Returns (domains, groups, paths, operations)."""
    if not load_version_manifest(version):
        return 0, 0, 0, 0
    check_layout(version)
    check_markdown(version)
    counts = check_specs(version) or (0, 0)
    check_common(version)
    groups = sum(len(d[2]) for d in version.domains)
    return (len(version.domains), groups) + tuple(counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--strict', action='store_true',
                        help='exit non-zero on warnings as well as errors')
    parser.add_argument('--version', metavar='vN.N',
                        help='validate only this version (the index is always checked)')
    args = parser.parse_args()

    versions = check_index()
    if args.version:
        if args.version not in [v.name for v in versions]:
            error('%s: not a version listed in manifest.json' % args.version)
        versions = [v for v in versions if v.name == args.version]

    totals = [0, 0, 0, 0]
    for version in versions:
        for i, n in enumerate(check_version(version)):
            totals[i] += n

    print('versions=%d domains=%d groups=%d paths=%d operations=%d errors=%d warnings=%d'
          % ((len(versions),) + tuple(totals) + (len(errors), len(warnings))))
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
