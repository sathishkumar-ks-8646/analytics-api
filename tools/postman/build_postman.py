#!/usr/bin/env python3
"""
build_postman.py - Generate the Zoho Analytics REST API Postman collection and environment for one
API version of this repository, from the artefacts already built for that version.

Inputs  (<repo>/<VERSION>/):
  okf/references/endpoint-catalog.json   every endpoint: title, method, path, scopes, org header, CONFIG
                                         location, success status, permission, document paths
  okf/domains/**/*.md                    endpoint descriptions (frontmatter) and group descriptions
  okf/workflows/*.md                     playbooks: title, description, steps, the endpoints they use
  oas/<domain>-grouped-api.json          CONFIG examples, header parameters, multipart parts
  md/<domain>/<GROUP>.md                 the opening paragraph of each group document
  manifest.json                          domain order, Postman emoji / title / "covers" text
  tools/postman/templates/               the Authentication folder, collection scripts, long descriptions
  tools/postman/api-reference-links.json endpoint title -> page in the public API reference (curated)
Output  (<repo>/<VERSION>/postman/):
  Zoho Analytics REST APIs.postman_collection.json
  Zoho Analytics REST Variables.postman_environment.json

Usage:
  python3 tools/postman/build_postman.py                  # the `latest` version in <repo>/manifest.json
  python3 tools/postman/build_postman.py --version v2.0
  python3 tools/postman/build_postman.py --check          # build in memory and diff against the files on disk

Standard library only. Re-running regenerates both files; nothing in <VERSION>/postman/ is edited by hand.
"""
import argparse, collections, glob, json, os, re, sys, uuid
from urllib.parse import unquote

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL_DIR))
TEMPLATES = os.path.join(TOOL_DIR, 'templates')

COLLECTION_NAME = 'Zoho Analytics REST APIs'
ENVIRONMENT_NAME = 'Zoho Analytics REST Variables'
SCHEMA = 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
# Where the published OpenAPI lives, for endpoints that have no page in the API reference yet.
OAS_PUBLIC_BASE = 'https://github.com/zoho/analytics-oas/blob/main'

ORG_HEADER = 'ZANALYTICS-ORGID'
ORG_HEADER_DESC = 'Organization ID. Get it from **Get Org List**.'
# Header parameters other than the organization header, by OpenAPI parameter name.
HEADER_VARS = {
    'dest-org-id': ('ZANALYTICS-DEST-ORGID', 'dest-organization-id',
                    'Destination organization ID. Enable this header (and the `dest-organization-id` '
                    'environment variable) only to copy into another organization you administer.'),
}
HEADER_VARS['ZANALYTICS-DEST-ORGID'] = HEADER_VARS['dest-org-id']   # the same header declared inline
# Environment variables that are always on, in display order: (name, initial value).
ALWAYS_ON = [
    ('analytics-domain', 'analyticsapi.zoho.com'),
    ('accounts-domain', 'accounts.zoho.com'),
    ('client-id', ''), ('client-secret', ''), ('redirect-uri', ''),
    ('access-token', ''), ('refresh-token', ''), ('expiry-time', ''),
    ('organization-id', ''),
]
# Identifier variables that exist even though no path parameter carries them.
EXTRA_IDENTIFIERS = ['dest-organization-id', 'job-id']


# ----------------------------------------------------------------------------- helpers

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


def frontmatter(text):
    """Flat `key: value` pairs of a YAML frontmatter block (enough for title and description)."""
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    meta = {}
    if not m:
        return meta
    for line in m.group(1).split('\n'):
        mm = re.match(r'^([a-z_]+): (.*)$', line)
        if mm:
            v = mm.group(2).strip()
            if v.startswith('"') and v.endswith('"'):
                try:
                    v = json.loads(v)
                except Exception:
                    v = v.strip('"')
            meta[mm.group(1)] = v
    return meta


def first_paragraph(text):
    parts = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    return parts[0].replace('\n', ' ') if parts else ''


def scope_short(scope):
    return scope.split('ZohoAnalytics.', 1)[1] if scope.startswith('ZohoAnalytics.') else scope


def scope_family(scope):
    return scope_short(scope).split('.')[0]


def pm_var(name):
    return '{{' + name + '}}'


def path_to_postman(path):
    return re.sub(r'\{([^}]+)\}', lambda m: pm_var(m.group(1)), path)


def deref(doc, obj):
    if isinstance(obj, dict) and '$ref' in obj and obj['$ref'].startswith('#/'):
        node = doc
        for part in obj['$ref'][2:].split('/'):
            node = node[part.replace('~1', '/').replace('~0', '~')]
        return node
    return obj


def pretty(value):
    return json.dumps(value, indent=2, ensure_ascii=False)


def compact(value):
    return json.dumps(value, ensure_ascii=False)


# ----------------------------------------------------------------------------- sources

class Sources:
    def __init__(self, version):
        self.version = version
        self.vdir = os.path.join(ROOT, version)
        self.manifest = load(os.path.join(self.vdir, 'manifest.json'))
        self.okf = os.path.join(self.vdir, 'okf')
        catalog_path = os.path.join(self.okf, 'references', 'endpoint-catalog.json')
        if not os.path.isfile(catalog_path):
            sys.exit(f'{catalog_path} not found. Build the OKF bundle first: python3 tools/okf/build_okf.py --version {version}')
        self.catalog = load(catalog_path)
        self.endpoints = self.catalog['endpoints']
        self.oas = {}
        for f in sorted(glob.glob(os.path.join(self.vdir, 'oas', '*.json'))):
            self.oas[os.path.basename(f)] = load(f)
        self.ops = {}
        for fname, doc in self.oas.items():
            for path, item in doc.get('paths', {}).items():
                for method, op in item.items():
                    if method in ('get', 'post', 'put', 'delete', 'patch'):
                        self.ops[(method.upper(), path)] = (doc, op, item.get('parameters', []))
        self.links = load(os.path.join(TOOL_DIR, 'api-reference-links.json')) if os.path.isfile(os.path.join(TOOL_DIR, 'api-reference-links.json')) else {}
        self.workflows = self._workflows()

    # -- OKF documents
    def doc_meta(self, bundle_path):
        p = os.path.join(self.okf, bundle_path.lstrip('/'))
        return frontmatter(read(p)) if os.path.isfile(p) else {}

    def group_description(self, dslug, gslug):
        return self.doc_meta(f'/domains/{dslug}/{gslug}/overview.md').get('description', '')

    def domain_description(self, dslug):
        return self.doc_meta(f'/domains/{dslug}/overview.md').get('description', '')

    def group_preamble(self, folder, md_stem):
        """Opening paragraph of the group's source document, re-addressed to the Postman folder."""
        p = os.path.join(self.vdir, 'md', folder, md_stem + '.md')
        if not os.path.isfile(p):
            return ''
        body = re.sub(r'^# .*\n', '', read(p), count=1)
        para = first_paragraph(body)
        para = re.sub(r'^This (document|file|page) (covers|describes)', 'This section covers', para)
        para = re.sub(r'\]\(([A-Z_]+\.md)(#[^)]*)?\)', ']()', para)      # cross-file links do not resolve here
        para = re.sub(r'\[([^\]]+)\]\(\)', r'\1', para)
        return para

    def _workflows(self):
        out = []
        for f in sorted(glob.glob(os.path.join(self.okf, 'workflows', '*.md'))):
            if os.path.basename(f) == 'index.md':
                continue
            text = read(f)
            meta = frontmatter(text)
            steps = []
            m = re.search(r'\n# Steps[^\n]*\n(.*?)(\n# |\Z)', text, re.S)
            if m:
                for line in m.group(1).split('\n'):
                    mm = re.match(r'^\d+\.\s+\*\*(.+?)\*\*', line) or re.match(r'^\d+\.\s+([^.:\[]{3,60}?)(?:[.:]| with | using |\s+\[)', line)
                    if mm:
                        steps.append(mm.group(1).rstrip('.').rstrip(',').strip())
            docs = set(re.findall(r'\]\((?:\.\./)*(?:/)?domains/([a-z0-9-]+)/([a-z0-9-]+)/[a-z0-9-]+\.md', text))
            out.append(dict(title=meta.get('title', os.path.basename(f)), description=meta.get('description', ''),
                            steps=steps, groups={(d, g) for d, g in docs}, domains={d for d, _ in docs}))
        return out

    # -- OpenAPI details for one endpoint
    def op(self, ep):
        return self.ops.get((ep['method'], ep['path']))

    def config_examples(self, ep):
        """[(summary, description, CONFIG value)] in declaration order, plus the other multipart parts
        of the first example, and the text of the CONFIG parameter's description for GET requests."""
        found = self.op(ep)
        if not found:
            return [], {}, ''
        doc, op, path_params = found
        examples, extra_parts, param_desc = [], {}, ''
        rb = op.get('requestBody')
        if rb:
            for ct, media in rb.get('content', {}).items():
                for ex in media.get('examples', {}).values():
                    ex = deref(doc, ex)
                    val = ex.get('value', {})
                    if isinstance(val, dict) and 'CONFIG' in val:
                        examples.append((ex.get('summary', ''), ex.get('description', ''), val['CONFIG']))
                        for k, v in val.items():          # first value seen for every other part
                            if k != 'CONFIG' and k not in extra_parts:
                                extra_parts[k] = v
                if not examples and 'example' in media:
                    val = media['example']
                    if isinstance(val, dict) and 'CONFIG' in val:
                        examples.append(('', '', val['CONFIG']))
                break
        for prm in list(op.get('parameters', [])) + list(path_params):
            prm = deref(doc, prm)
            if prm.get('name') == 'CONFIG' and prm.get('in') == 'query':
                param_desc = re.sub(r'\s*As this is a GET request, the value must be stringified and URL encoded before it is sent\.?', '', prm.get('description', '')).strip()
                for ex in prm.get('examples', {}).values():
                    ex = deref(doc, ex)
                    examples.append((ex.get('summary', ''), ex.get('description', ''), ex.get('value', {})))
                if not examples and 'example' in prm:
                    examples.append(('', '', prm['example']))
        return examples, extra_parts, param_desc

    def doc_config_example(self, ep):
        """For an endpoint with no OpenAPI operation: the first CONFIG value shown in its OKF document
        (a `CONFIG=<json>` line in a sample request, else the first JSON object in the Request section)."""
        p = os.path.join(self.okf, ep['doc'].lstrip('/'))
        if not os.path.isfile(p):
            return None
        text = read(p)
        for m in re.finditer(r'CONFIG=(\{.*?\}|%7B.*?%7D)(?=[\s&]|$)', text, re.M):
            try:
                return json.loads(unquote(m.group(1)))
            except ValueError:
                continue
        m = re.search(r'\n# Request\n(.*?)(\n# |\Z)', text, re.S)
        if m:
            for block in re.findall(r'```json\n(.*?)```', m.group(1), re.S):
                try:
                    v = json.loads(block)
                    if isinstance(v, dict):
                        return v
                except ValueError:
                    continue
        return None

    def header_params(self, ep):
        found = self.op(ep)
        if not found:
            return []
        doc, op, path_params = found
        out = []
        for prm in list(path_params) + list(op.get('parameters', [])):
            raw = prm
            prm = deref(doc, prm)
            if prm.get('in') != 'header':
                continue
            key = raw.get('$ref', '').rsplit('/', 1)[-1] or prm.get('name')
            out.append((key, prm.get('name'), bool(prm.get('required')), prm.get('description', '')))
        return out

    def multipart_schema(self, ep):
        found = self.op(ep)
        if not found:
            return {}
        doc, op, _ = found
        rb = op.get('requestBody') or {}
        media = rb.get('content', {}).get('multipart/form-data')
        if not media:
            return {}
        schema = deref(doc, media.get('schema', {}))
        return {k: deref(doc, v) for k, v in schema.get('properties', {}).items()}


# ----------------------------------------------------------------------------- rendering

def org_header_status(src, ep):
    """required / optional / not-required. The OpenAPI header parameter is authoritative when the
    operation exists (its `required` flag); the catalog's value is the fallback."""
    for key, name, req, desc in src.header_params(ep):
        if name == ORG_HEADER:
            return 'required' if req else 'optional'
    return ep.get('org_id_header') or 'not-required'


def scopes_of(src, ep):
    """The catalog's scopes, else the first scope named in the endpoint document (markdown-only endpoints)."""
    if ep.get('oauth_scopes'):
        return list(ep['oauth_scopes'])
    p = os.path.join(src.okf, ep['doc'].lstrip('/'))
    if os.path.isfile(p):
        m = re.search(r'`(ZohoAnalytics\.[a-z]+\.[a-z]+)`', read(p))
        if m:
            return [m.group(1)]
    return []


def request_description(src, ep, examples):
    meta = src.doc_meta(ep['doc'])
    summary = meta.get('description', '') or ep['title']
    rows = [('Endpoint', f"`{ep['method']} {ep['path']}`"),
            ('OAuth scope', ', '.join(f'`{s}`' for s in scopes_of(src, ep)) or '-')]
    org = org_header_status(src, ep)
    rows.append(('Org header', f'`{ORG_HEADER}` required' if org == 'required' else
                 (f'`{ORG_HEADER}` optional — scopes the result to one organization' if org == 'optional' else 'Not required')))
    cfg = ep.get('config_parameter') or {}
    loc = cfg.get('location', 'none')
    if loc != 'none':
        where = {'query': 'Query parameter', 'form': 'Body form field', 'multipart': 'Multipart form field'}.get(loc, loc)
        rows.append(('CONFIG', f"{where} · {'**mandatory**' if cfg.get('required') else 'optional'}"))
    status = ep.get('success_status')
    rows.append(('Success', f'`{status}` (no response body)' if status == 204 else f'`{status}`'))
    table = '\n'.join(['| | |', '| :--- | :--- |'] + [f'| **{k}** | {v} |' for k, v in rows])
    parts = [summary, table]
    perm = (ep.get('permission_required') or '').strip()
    if perm and not perm.lower().startswith('see '):
        parts.append(f'**Who can call it** — {perm}')
    others = [s for s, _, _ in examples[1:] if s]
    if others:
        parts.append('**Other ready-made CONFIG examples:** ' + ', '.join(f'*{s}*' for s in others) + ' — see the API reference.')
    link = src.links.get(ep['title'])
    if link:
        parts.append(f'📘 [API reference ↗]({link})')
    else:
        oas_file = (ep.get('openapi') or {}).get('file', '').rsplit('/', 1)[-1]
        if oas_file:
            parts.append(f'🆕 Newly added — not yet on the docs site. [OpenAPI definition ↗]({OAS_PUBLIC_BASE}/{src.version}/{oas_file})')
    return '\n\n'.join(parts)


def build_request(src, ep):
    examples, extra_parts, param_desc = src.config_examples(ep)
    cfg = ep.get('config_parameter') or {}
    if not examples and cfg.get('location', 'none') != 'none' and not src.op(ep):
        v = src.doc_config_example(ep)
        if v is not None:
            examples = [('', 'Example from the API reference.', v)]
    loc, required = cfg.get('location', 'none'), bool(cfg.get('required'))
    first = examples[0] if examples else None

    headers = []
    org = org_header_status(src, ep)
    if org in ('required', 'optional'):
        h = collections.OrderedDict(key=ORG_HEADER, value=pm_var('organization-id'),
                                    description=ORG_HEADER_DESC + (' Optional for this endpoint.' if org == 'optional' else ''))
        headers.append(h)
    for key, name, req, desc in src.header_params(ep):
        if name == ORG_HEADER:
            continue
        hname, var, hdesc = HEADER_VARS.get(key) or HEADER_VARS.get(name) or (name, key.lower(), desc)
        h = collections.OrderedDict(key=hname, value=pm_var(var), description=hdesc)
        if not req:
            h['disabled'] = True
        headers.append(h)

    url_path = path_to_postman(ep['path'])
    raw = 'https://' + pm_var('analytics-domain') + url_path
    url = collections.OrderedDict(raw=raw, protocol='https', host=[pm_var('analytics-domain')],
                                  path=[seg for seg in url_path.split('/') if seg])
    body = None
    if loc == 'query':
        value = first[2] if first is not None else {}
        # A mandatory CONFIG ships enabled with the first example; an optional one ships disabled
        # (the request works without it) and describes what it does rather than one example.
        q = collections.OrderedDict(key='CONFIG', value=compact(value),
                                    description=param_desc or (first[1] if first else 'Optional CONFIG JSON. URL encoded by the collection script.'))
        if not required:
            q['disabled'] = True
        url['query'] = [q]
        if 'disabled' not in q:
            url['raw'] = raw + '?CONFIG=' + compact(value)
    elif loc in ('form', 'multipart'):
        value = first[2] if first is not None else {}
        item = collections.OrderedDict(key='CONFIG', value=pretty(value), type='text')
        if loc == 'multipart':
            # the example description describes the whole multipart example, not the CONFIG part
            item['description'] = 'Import configuration. Mandatory.' if required else 'Import configuration.'
        elif first is not None and first[1]:
            item['description'] = first[1]
        if loc == 'form':
            body = collections.OrderedDict(mode='urlencoded', urlencoded=[item])
        else:
            parts = [item]
            schema = src.multipart_schema(ep)
            for name, prop in schema.items():
                if name == 'CONFIG':
                    continue
                desc = (prop.get('description') or '').split('\n')[0]
                if prop.get('format') == 'binary':
                    parts.append(collections.OrderedDict(key=name, type='file', description=desc, value=None))
                else:
                    p = collections.OrderedDict(key=name, type='text', value=str(extra_parts.get(name, '')), description=desc)
                    if name not in extra_parts or any(pp.get('format') == 'binary' for pp in schema.values()):
                        p['disabled'] = True   # FILE is the enabled alternative; DATA ships disabled
                    parts.append(p)
            body = collections.OrderedDict(mode='formdata', formdata=parts)

    request = collections.OrderedDict(method=ep['method'], header=headers)
    if body is not None:
        request['body'] = body
    request['url'] = url
    request['description'] = request_description(src, ep, examples)
    return collections.OrderedDict(name=ep['title'], request=request, response=[])


def steps_arrow(wf):
    return ' → '.join(wf['steps']) if wf['steps'] else ''


def group_folder(src, domain, group, eps):
    dslug, gslug, gtitle = domain['okf']['slug'], group['okf']['slug'], group['okf']['title']
    rows = ['| # | API | Method | Path | Scope |', '| ---: | :--- | :--- | :--- | :--- |']
    for i, ep in enumerate(eps, 1):
        scopes = ', '.join(f'`{scope_short(s)}`' for s in scopes_of(src, ep)) or '-'
        rows.append(f"| {i} | **{ep['title']}** | `{ep['method']}` | `{ep['path']}` | {scopes} |")
    text = [f'## {gtitle}', '', src.group_preamble(domain['folder'], group['md']) or src.group_description(dslug, gslug), '',
            '### APIs in this section', '', '\n'.join(rows)]
    wfs = [w for w in src.workflows if (dslug, gslug) in w['groups']]
    if wfs:
        text += ['', '### Workflows that use these APIs', '']
        for w in wfs:
            text.append(f"- **{w['title']}** — {w['description']}  \n  `{steps_arrow(w)}`")
    return collections.OrderedDict(name=gtitle, item=[build_request(src, ep) for ep in eps], description='\n'.join(text))


def domain_folder(src, domain, by_group):
    dslug = domain['okf']['slug']
    pm = domain.get('postman', {})
    title = pm.get('title', domain['okf']['title'])
    name = (pm.get('emoji', '') + ' ' + title).strip()
    folders, total, families = [], 0, collections.Counter()
    sections = ['| Section | APIs | What it covers |', '| :--- | ---: | :--- |']
    for group in domain['groups']:
        eps = by_group.get((dslug, group['okf']['slug']), [])
        if not eps:
            continue
        folders.append(group_folder(src, domain, group, eps))
        total += len(eps)
        for ep in eps:
            for s in scopes_of(src, ep):
                families[scope_family(s)] += 1
        sections.append(f"| **{group['okf']['title']}** | {len(eps)} | {src.group_description(dslug, group['okf']['slug'])} |")
    fam = ', '.join(f'`{f}.*`' for f, _ in sorted(families.items(), key=lambda kv: (-kv[1], kv[0])))
    text = [f'# {name}', '', src.domain_description(dslug), '',
            f'> **{total} APIs** in **{len(folders)} sections** · scopes {fam}', '',
            '### Sections', '', '\n'.join(sections)]
    wfs = [w for w in src.workflows if dslug in w['domains']]
    if wfs:
        text += ['', '### Workflows', '', '| Playbook | Call sequence |', '| :--- | :--- |']
        for w in wfs:
            text.append(f"| **{w['title']}**<br/>{w['description']} | {steps_arrow(w)} |")
    return collections.OrderedDict(name=name, item=folders, description='\n'.join(text)), total, len(folders)


def fill_counts(template, total_requests, total_apis, domains, sections, domain_rows):
    """Substitute the numbers and the per-domain table of a long description template."""
    t = template
    t = re.sub(r'\*\*\d+ API requests\*\* · \*\*\d+ domains\*\* · \*\*\d+ sections\*\*',
               f'**{total_requests} API requests** · **{domains} domains** · **{sections} sections**', t)
    t = re.sub(r'\*\*\d+ APIs\*\* · \*\*\d+ domains\*\* · \*\*\d+ sections\*\*',
               f'**{total_apis} APIs** · **{domains} domains** · **{sections} sections**', t)
    # The "What's inside" table: replace every existing domain row with the generated ones.
    m = re.search(r'(\| Domain \| APIs \| Sections(?: \| Covers)? \|\n\| ---.*?\n)((?:\|.*\n)+)', t)
    if m:
        t = t[:m.start(2)] + '\n'.join(domain_rows) + '\n' + t[m.end(2):]
    return t


def build(version):
    src = Sources(version)
    manifest = src.manifest
    by_group = collections.defaultdict(list)
    for ep in src.endpoints:
        by_group[(ep['domain'], ep['group'])].append(ep)

    auth_folder = load(os.path.join(TEMPLATES, 'authentication-folder.json'))
    skeleton = load(os.path.join(TEMPLATES, 'collection-skeleton.json'))
    coll_desc = read(os.path.join(TEMPLATES, 'collection-description.md'))
    ver_desc = read(os.path.join(TEMPLATES, 'version-folder-description.md'))

    domain_folders, total_apis, total_sections = [], 0, 0
    rows_short, rows_long = [], []
    for domain in manifest['domains']:
        folder, n, s = domain_folder(src, domain, by_group)
        if not folder['item']:
            continue
        domain_folders.append(folder)
        total_apis += n
        total_sections += s
        pm = domain.get('postman', {})
        title = pm.get('title', domain['okf']['title'])
        rows_short.append(f'| **{title}** | {n} | {s} |')
        rows_long.append(f"| **{(pm.get('emoji', '') + ' ' + title).strip()}** | {n} | {s} | {pm.get('covers', '')} |")

    auth_count = len(auth_folder.get('item', []))
    api_version = manifest.get('api_version', 'v2')
    version_folder = collections.OrderedDict(
        name=f'2️⃣ {version}' if api_version == 'v2' else f'{version}',
        item=domain_folders,
        description=fill_counts(ver_desc, total_apis + auth_count, total_apis, len(domain_folders), total_sections, rows_long))

    existing = os.path.join(ROOT, version, 'postman', f'{COLLECTION_NAME}.postman_collection.json')
    postman_id = None
    if os.path.isfile(existing):
        try:
            postman_id = load(existing)['info'].get('_postman_id')
        except Exception:
            postman_id = None
    info = collections.OrderedDict(_postman_id=postman_id or str(uuid.uuid4()), name=COLLECTION_NAME,
                                   description=fill_counts(coll_desc, total_apis + auth_count, total_apis, len(domain_folders), total_sections, rows_short),
                                   schema=skeleton.get('info_schema', SCHEMA))
    collection = collections.OrderedDict(info=info, item=[auth_folder, version_folder])
    if skeleton.get('auth'):
        collection['auth'] = skeleton['auth']
    if skeleton.get('event'):
        collection['event'] = skeleton['event']

    # Environment: every identifier that appears in a path, plus the always-on variables.
    identifiers = []
    for ep in src.endpoints:
        for name in re.findall(r'\{([^}]+)\}', ep['path']):
            if name not in identifiers:
                identifiers.append(name)
    for name in EXTRA_IDENTIFIERS:
        if name not in identifiers:
            identifiers.append(name)
    values = [collections.OrderedDict(key=k, value=v, type='default', enabled=True) for k, v in ALWAYS_ON]
    values += [collections.OrderedDict(key=k, value='', type='default', enabled=False) for k in identifiers]
    environment = collections.OrderedDict(name=ENVIRONMENT_NAME, values=values, _postman_variable_scope='environment')
    return collection, environment, dict(requests=total_apis, domains=len(domain_folders), sections=total_sections)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', help='API version directory (default: `latest` in <repo>/manifest.json)')
    ap.add_argument('--out', help='output directory (default <repo>/<VERSION>/postman)')
    ap.add_argument('--check', action='store_true', help='do not write; exit 1 if the files on disk differ from what would be generated')
    a = ap.parse_args()
    version = a.version or os.environ.get('API_VERSION') or load(os.path.join(ROOT, 'manifest.json'))['latest']
    collection, environment, counts = build(version)
    out = a.out or os.path.join(ROOT, version, 'postman')
    files = {f'{COLLECTION_NAME}.postman_collection.json': collection,
             f'{ENVIRONMENT_NAME}.postman_environment.json': environment}
    if a.check:
        rc = 0
        for name, payload in files.items():
            p = os.path.join(out, name)
            current = read(p) if os.path.isfile(p) else None
            fresh = json.dumps(payload, indent=1, ensure_ascii=False) + '\n'
            if current != fresh:
                # the collection id is carried over, so any difference is content
                print(f'STALE  {os.path.relpath(p, ROOT)}')
                rc = 1
            else:
                print(f'ok     {os.path.relpath(p, ROOT)}')
        sys.exit(rc)
    os.makedirs(out, exist_ok=True)
    for name, payload in files.items():
        with open(os.path.join(out, name), 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=1, ensure_ascii=False)
            f.write('\n')
    print(f"requests={counts['requests']} domains={counts['domains']} sections={counts['sections']} -> {os.path.relpath(out, ROOT)}/")


if __name__ == '__main__':
    main()
