#!/usr/bin/env python3
"""
build_okf.py - Generates the Zoho Analytics REST API Open Knowledge Format (OKF v0.2) bundle
for one API version of this repository.

Inputs  (<repo>/<VERSION>/, the authored source documents of that API version):
  md/<domain>/<GROUP>.md                              rich narrative docs, one file per API group
  zenesis-oas/<domain>-grouped-api.json               OpenAPI 3 specs, one file per domain
  zenesis-oas/common/zoho-analytics-api-common.json   shared OAuth scopes, error envelope, common responses
  zenesis-oas-samples/*-samples.json                  SDK snippets keyed by path + method
  manifest.json                                       the domain / group inventory (drives DOMAINS below)
  tools/okf/handwritten/<VERSION>/**                  hand-written concepts copied into the bundle
Output  (<repo>/<VERSION>/okf): the OKF bundle. Deleted and regenerated on every run.

Usage:
  python3 tools/okf/build_okf.py                 # the `latest` version named in <repo>/manifest.json
  python3 tools/okf/build_okf.py --version v2.0  # one version (or API_VERSION=v2.0 in the environment)
  OKF_BUNDLE_VERSION=1.4.0 python3 tools/okf/build_okf.py   # set the bundle's content version
"""
import json, re, os, sys, glob, shutil, html, collections, datetime
from html.parser import HTMLParser

TOOL_DIR  = os.path.dirname(os.path.abspath(__file__))                       # <repo>/tools/okf
ROOT      = os.path.dirname(os.path.dirname(TOOL_DIR))                       # repository root


def _select_version():
    """--version vN.N, else API_VERSION, else `latest` from the repository manifest."""
    args = sys.argv[1:]
    if '--version' in args:
        return args[args.index('--version') + 1]
    for a in args:
        if a.startswith('--version='):
            return a.split('=', 1)[1]
    if os.environ.get('API_VERSION'):
        return os.environ['API_VERSION']
    with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as f:
        return json.load(f)['latest']


VERSION   = _select_version()
SRC       = os.path.join(ROOT, VERSION)
MD_DIR    = os.path.join(SRC, 'md')
OAS_DIR   = os.path.join(SRC, 'zenesis-oas')
SAMP_DIR  = os.path.join(SRC, 'zenesis-oas-samples')
COMMON    = os.path.join(OAS_DIR, 'common', 'zoho-analytics-api-common.json')
HAND      = os.path.join(TOOL_DIR, 'handwritten', VERSION)
OUT       = os.path.join(SRC, 'okf')
VERSION_MANIFEST = os.path.join(SRC, 'manifest.json')

if not os.path.isdir(OAS_DIR):
    sys.exit('%s does not exist: is VERSION=%s right? Versions are the vN.N/ directories '
             'listed in %s' % (OAS_DIR, VERSION, os.path.join(ROOT, 'manifest.json')))
if not os.path.isdir(HAND):
    sys.exit('%s does not exist: every version needs its own hand-written concepts. '
             'Copy tools/okf/handwritten/<previous version>/ and revise it.' % HAND)

with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as _f:
    REPO_MANIFEST = json.load(_f)
with open(VERSION_MANIFEST, encoding='utf-8') as _f:
    MANIFEST = json.load(_f)
API_VERSION = MANIFEST.get('api_version', 'v2')
# Raw-file base used for the absolute links in llms.txt. The bundle is copied unchanged into the
# public repository, so the links point there: `publish.okf.raw_base` of this version's entry in
# <repo>/manifest.json (override with OKF_RAW_BASE); else this repository's own raw base.
_entry = next((v for v in REPO_MANIFEST.get('versions', []) if v.get('version') == VERSION), {})
OKF_RAW_BASE = (os.environ.get('OKF_RAW_BASE')
                or (_entry.get('publish') or {}).get('okf', {}).get('raw_base')
                or (REPO_MANIFEST.get('raw_base', '').rstrip('/') + '/' + VERSION + '/okf'))

BUILDER   = 'claude-fable-5.1/okf-builder-1.0'
NOW       = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
BASE_URL  = 'https://analyticsapi.zoho.com'
# OKF v0.2 §5.2 requires `by` inside `generated`; §7 fixes its spelling. Trust tiers (§5.3)
# are derived from this prefix, so an actorless generated block is not merely incomplete.
ACTOR     = 'process:build_okf'
MISSING_PERMISSION = []
OKF_VERSION    = '0.2'


def _default_bundle_version():
    """OKF_BUNDLE_VERSION, else the version of the bundle already on disk, else 1.0.0.
    Rebuilding never silently regresses the content version; bump it deliberately."""
    if os.environ.get('OKF_BUNDLE_VERSION'):
        return os.environ['OKF_BUNDLE_VERSION']
    existing = os.path.join(OUT, 'manifest.json')
    if os.path.isfile(existing):
        try:
            with open(existing, encoding='utf-8') as f:
                return json.load(f)['version']
        except Exception:
            pass
    return '1.0.0'


BUNDLE_VERSION = _default_bundle_version()
SOURCE_AUTHOR = 'team:zoho-analytics-api-docs'

# --------------------------------------------------------------------------------------------
# Static configuration
# --------------------------------------------------------------------------------------------
# Ordered list of (md folder, domain slug, domain title, OpenAPI file, [(md file stem, group slug, group title), ...]).
# Read from <VERSION>/manifest.json: the `okf` block of each domain and group holds the slug and
# title used in the bundle. Adding a group or domain starts there, not here.
DOMAINS = [
    (d['folder'], d['okf']['slug'], d['okf']['title'], d['slug'] + '-grouped-api.json',
     [(g['md'], g['okf']['slug'], g['okf']['title']) for g in d['groups']])
    for d in MANIFEST['domains']
]

# Legacy cross-file link names used inside the markdown docs -> group slug
LEGACY_ALIAS = {
  'ROW': 'row-operations', 'ORG_INFO': 'org-info-and-settings', 'TRASH': 'trash-management',
  'SLIDESHOW': 'slideshow-management', 'EMBEDURL': 'embed-url', 'DOMAIN_AND_WHITELABEL': 'domain-and-white-label',
  'AUTOML': 'automl', 'AUTOML_ANALYSIS': 'automl',
}

# OpenAPI operation title -> markdown endpoint title (where they differ)
TITLE_MAP = {
 'Update Rows': 'Update Row',
 'Import Data into a New Table': 'Import Data into a New Table (Synchronous)',
 'Import Data into an Existing Table': 'Import Data into an Existing Table (Synchronous)',
 'Create Import Job for a New Table': 'Create Import Job for a New Table (Asynchronous)',
 'Create Import Job for an Existing Table': 'Create Import Job for an Existing Table (Asynchronous)',
 'Create Export Job using SQL Query': 'Create Export Job using SQL Query (Asynchronous)',
 'Create Export Job using View ID': 'Create Export Job using View ID (Asynchronous)',
 'Get Organizations': 'Get Org List',
 'Remove Share': 'Remove Shared Views',
 'Update Shared Details For View': 'Update Shared Details',
 'Get Shared Details For Views': 'Get Shared Details',
 'Get User Permissions': 'Get My Permissions',
 'Make Views Public': 'Make View Public',
 'Create Slideshow': 'Create Slide Show',
 'Get Slideshows': 'Get Slide List',
 'Update Slideshow': 'Update Slide Show',
 'Delete Slideshow': 'Delete Slide Show',
 'Get Slideshow Details': 'Get Slide Info',
 'Get Slideshow URL': 'Get Slide URL',
 'Add Favorite View': 'Add Favourite View',
 'Remove Favorite View': 'Remove Favourite View',
}
# Markdown-only endpoints (absent from the OpenAPI files) -> synthesized operation ids
MD_ONLY_OPS = {
 'Fetch All Embed URLs': 'getEmbedUrls',
 'Delete Embed URL': 'deleteEmbedUrl',
}

LANG_FENCE = {'Curl': 'bash', 'C#': 'csharp', 'Go': 'go', 'Java': 'java', 'Php': 'php', 'Python': 'python',
              'Node': 'javascript', 'Ruby': 'ruby', 'Deluge': 'deluge'}
LANG_TITLE = {'Curl': 'cURL', 'C#': 'C#', 'Go': 'Go', 'Java': 'Java', 'Php': 'PHP', 'Python': 'Python',
              'Node': 'Node.js', 'Ruby': 'Ruby', 'Deluge': 'Deluge (Zoho scripting)'}

# Default HTTP status inferred for an error code when no sample response states it
DEFAULT_HTTP = {'7301': 403, '8535': 401, '7005': 500, '7103': 404, '7104': 404, '8023': 403, '8241': 409}

# How each identifier is obtained (used by foundations/identifiers.md)
ID_SOURCES = {
 'ZANALYTICS-ORGID': ('Organization ID', ['Get Org List', 'Get Meta Details From Name']),
 'ZANALYTICS-DEST-ORGID': ('Destination organization ID for cross-organization copies', ['Get Org List']),
 'workspace-id': ('Workspace ID', ['Get Meta Details From Name', 'Get All Workspace List', 'Get Owned Workspace List', 'Get Shared Workspace List', 'Create Workspace']),
 'view-id': ('View ID (table, report, dashboard, query table, etc.)', ['Get Meta Details From Name', 'Get View List', 'Create Table', 'Create Query Table', 'Import Data into a New Table (Synchronous)', 'Create Report', 'Create Dashboard']),
 'column-id': ('Column ID within a table', ['Get Table Metadata', 'Add Column']),
 'folder-id': ('Folder ID within a workspace', ['Get Folder List', 'Create Folder']),
 'group-id': ('Workspace group ID', ['Get Group List', 'Create Group']),
 'job-id': ('Import or export job ID', ['Create Export Job using SQL Query (Asynchronous)', 'Create Export Job using View ID (Asynchronous)', 'Create Import Job for a New Table (Asynchronous)', 'Create Import Job for an Existing Table (Asynchronous)']),
 'datasource-id': ('Datasource ID', ['Get Datasources']),
 'schedule-id': ('Email schedule ID', ['Get Email Schedules', 'Create Email Schedule']),
 'querytable-id': ('Query table ID (a view ID)', ['Get Query Tables', 'Create Query Table']),
 'formula-id': ('Custom formula column ID or aggregate formula ID', ['Get Custom Formulas', 'Add Custom Formula', 'Get Aggregate Formula', 'Add Aggregate Formula', 'Get Unified Metrics in Workspace']),
 'variable-id': ('Workspace variable ID', ['Get Variables', 'Create Variable']),
 'slide-id': ('Slideshow ID', ['Get Slide List', 'Create Slide Show']),
 'analysis-id': ('AutoML analysis ID', ['Get AutoML Analysis In Org', 'Get AutoML Analysis In Workspace', 'Create AutoML Analysis']),
 'model-id': ('AutoML model ID', ['Get AutoML Analysis Details']),
 'deployment-id': ('AutoML model deployment ID', ['Get Deployments For A Model', 'Create AutoML Analysis Deployment']),
 'role-id': ('Custom role ID', []),
 'dashboard-id': ('Dashboard ID (a view ID whose type is Dashboard)', ['Get All Dashboards', 'Get Owned Dashboards', 'Get Shared Dashboards', 'Create Dashboard', 'Get View List']),
 'report-id': ('Report ID (a view ID of an analysis view)', ['Get View List', 'Create Report']),
}

# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------
def slugify(s):
    s = re.sub(r'`', '', s)
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9 _-]', '', s)
    return s.replace(' ', '-')

def overview_anchor(stitle):
    return slugify(re.sub(r'^Appendix [A-Z]\s*[–:-]\s*', '', stitle))

def kebab(s):
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', s)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)
    s = re.sub(r'[^A-Za-z0-9]+', '-', s)
    return s.strip('-').lower()

def yq(s):
    """YAML-safe scalar (JSON strings are valid YAML double-quoted scalars)."""
    if isinstance(s, bool): return 'true' if s else 'false'
    if isinstance(s, (int, float)): return str(s)
    if s is None: return 'null'
    s = str(s)
    if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9 _./:+()&-]*', s) and s.lower() not in ('true','false','null','yes','no','on','off') and not re.fullmatch(r'[0-9.]+', s) and ': ' not in s and ' #' not in s:
        return s
    return json.dumps(s, ensure_ascii=False)

def yaml_dump(obj, indent=0):
    pad = '  ' * indent
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                if not v: out.append(f'{pad}{k}: {{}}'); continue
                out.append(f'{pad}{k}:'); out.append(yaml_dump(v, indent + 1))
            elif isinstance(v, list):
                if not v: out.append(f'{pad}{k}: []'); continue
                out.append(f'{pad}{k}:')
                for it in v:
                    if isinstance(it, dict):
                        lines = yaml_dump(it, indent + 2).split('\n')
                        out.append(f'{pad}  - ' + lines[0].lstrip())
                        out.extend(lines[1:])
                    else:
                        out.append(f'{pad}  - {yq(it)}')
            else:
                out.append(f'{pad}{k}: {yq(v)}')
    return '\n'.join(out)

def ensure_generated_by(txt):
    """Add `by:` to a frontmatter `generated:` block that lacks it (OKF v0.2 §5.2).

    Hand-written concepts are copied verbatim, so they never pass through frontmatter().
    A `generated` block with no actor leaves consumers unable to derive a trust tier (§5.3).
    """
    if not txt.startswith('---\n'):
        return txt
    end = txt.find('\n---\n', 3)
    if end == -1:
        return txt
    fm, rest = txt[4:end + 1], txt[end + 1:]
    if re.search(r'(?m)^generated:', fm):
        if not re.search(r'(?m)^generated:\n(?:[ \t]+.*\n)*?[ \t]+by:', fm):
            fm = re.sub(r'(?m)^(generated:\n)', rf'\g<1>  by: {ACTOR}\n', fm, count=1)
    else:
        fm = fm.rstrip('\n') + f'\ngenerated:\n  by: {ACTOR}\n  at: {NOW}\n'
    return '---\n' + fm + rest

def frontmatter(meta):
    meta = collections.OrderedDict((k, v) for k, v in meta.items() if v not in (None, [], {}))
    if 'generated' not in meta:
        meta['generated'] = collections.OrderedDict(by=ACTOR, at=NOW)
    elif isinstance(meta['generated'], dict) and not meta['generated'].get('by'):
        # A hand-written concept may already carry `generated.at` without an actor.
        # §5.2 requires `by`, so fill it in, keeping `by` ahead of `at`.
        g = collections.OrderedDict(by=ACTOR)
        g.update(meta['generated'])
        meta['generated'] = g
    if 'status' in meta:  # keep status last
        meta.move_to_end('status')
    return '---\n' + yaml_dump(meta) + '\n---\n'

def first_sentence(text):
    text = re.sub(r'\s+', ' ', re.sub(r'[*`>]', '', text or '')).strip()
    m = re.match(r'(.+?[.!?])(\s|$)', text)
    return (m.group(1) if m else text)[:400]

def strip_md(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    return re.sub(r'[*`_]', '', text).strip()

def rel(from_path, to_path):
    return os.path.relpath(to_path, os.path.dirname(from_path))

def relativize_links(path, text):
    """Rewrite bundle-root links (`](/foundations/x.md)`) in the BODY of a document to paths
    relative to that document, so they resolve on GitHub, in a clone and under any raw base.
    Frontmatter is left alone: `resource`, `sources[].resource` and `api.openapi.file` stay
    bundle-root paths by contract. Fenced code is never touched."""
    fm, body = '', text
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        if end != -1:
            fm, body = text[:end + 5], text[end + 5:]
    here = os.path.dirname(path)
    def repl(m):
        target, anchor = m.group(1), m.group(2) or ''
        rel = os.path.relpath(os.path.join(OUT, target.lstrip('/')), here)
        if target.endswith('/') and not rel.endswith('/'): rel += '/'
        return '](' + rel + anchor + ')'
    out, fence = [], False
    for line in body.split('\n'):
        if line.lstrip().startswith('```'): fence = not fence
        if not fence:
            line = re.sub(r'\]\((/[^)\s#]*)(#[^)\s]*)?\)', repl, line)
        out.append(line)
    return fm + '\n'.join(out)

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if path.endswith('.md'):
        content = re.sub(r'\n{3,}', '\n\n', content)
        if os.path.abspath(path).startswith(os.path.abspath(OUT) + os.sep):
            content = relativize_links(path, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content if content.endswith('\n') else content + '\n')

def shift_headings(text, delta):
    """Shift markdown heading levels (delta<0 promotes). Skips fenced code."""
    out, fence = [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            fence = not fence
        if not fence:
            m = re.match(r'^(#{1,6}) (.*)$', line)
            if m:
                lvl = max(1, min(6, len(m.group(1)) + delta))
                line = '#' * lvl + ' ' + m.group(2)
        out.append(line)
    return '\n'.join(out)

def md_table(headers, rows):
    if not rows: return ''
    esc = lambda c: str(c).replace('|', '\\|').replace('\n', ' ')
    lines = ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---'] * len(headers)) + '|']
    for r in rows: lines.append('| ' + ' | '.join(esc(c) for c in r) + ' |')
    return '\n'.join(lines)

class _HTML2MD(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.in_li = False
    def handle_starttag(self, tag, attrs):
        if tag == 'li': self.out.append('\n- '); self.in_li = True
        elif tag == 'br': self.out.append('\n')
        elif tag in ('b', 'strong'): self.out.append('**')
        elif tag == 'code': self.out.append('`')
        elif tag == 'p': self.out.append('\n\n')
        elif tag == 'ul': self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('b', 'strong'): self.out.append('**')
        elif tag == 'code': self.out.append('`')
        elif tag == 'li': self.in_li = False
        elif tag in ('ul', 'p', 'blockquote'): self.out.append('\n')
    def handle_data(self, d): self.out.append(d)

def html_to_md(h):
    p = _HTML2MD(); p.feed(h); txt = html.unescape(''.join(p.out))
    txt = re.sub(r'\*\*\s*\*\*', '', txt)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n')]
    lines = [l for l in lines if l]
    lines = [l for l in lines if l.lower().rstrip(':') not in ('note', 'notes')]
    return '\n'.join(lines)

# --------------------------------------------------------------------------------------------
# Load OpenAPI + samples + common
# --------------------------------------------------------------------------------------------
common = json.load(open(COMMON))
SCOPES = common['components']['securitySchemes']['iam-oauth2-schema']['flows']['authorizationCode']['scopes']

def deref(doc, obj):
    if isinstance(obj, dict) and '$ref' in obj and obj['$ref'].startswith('#/'):
        node = doc
        for part in obj['$ref'][2:].split('/'):
            node = node[part.replace('~1', '/').replace('~0', '~')]
        return node
    return obj

OAS = {}          # oas filename -> doc
OPS = {}          # md title -> op record
for _, dslug, dtitle, oasfile, groups in DOMAINS:
    doc = json.load(open(os.path.join(OAS_DIR, oasfile)))
    OAS[oasfile] = doc
    sfile = os.path.join(SAMP_DIR, oasfile.replace('.json', '-samples.json'))
    samples = json.load(open(sfile)) if os.path.exists(sfile) else {}
    for path, ops in doc['paths'].items():
        for method, op in ops.items():
            if method not in ('get', 'post', 'put', 'delete', 'patch'): continue
            title = (op.get('x-zenesis-title') or op['summary']).strip()
            mdtitle = TITLE_MAP.get(title, title)
            params = [deref(doc, p) for p in op.get('parameters', [])]
            scopes = [s for sec in op.get('security', []) for s in sec.get('iam-oauth2-schema', [])]
            rb = op.get('requestBody')
            req_ct, config_loc, config_req, body_props = None, 'none', False, {}
            for p in params:
                if p.get('name') == 'CONFIG' and p.get('in') == 'query':
                    config_loc, config_req = 'query', bool(p.get('required'))
            if rb:
                for ct, cv in rb.get('content', {}).items():
                    req_ct = ct
                    sch = deref(doc, cv.get('schema', {}))
                    body_props = sch.get('properties', {})
                    if 'CONFIG' in body_props:
                        config_loc = 'multipart' if 'multipart' in ct else 'form'
                        config_req = 'CONFIG' in sch.get('required', [])
            resp = op.get('responses', {})
            success = next((c for c in ('200', '201', '204') if c in resp), None)
            resp_ct = list(resp.get(success, {}).get('content', {}).keys()) if success else []
            resp_schema = None
            if success and 'application/json' in resp.get(success, {}).get('content', {}):
                rs = resp[success]['content']['application/json'].get('schema', {})
                resp_schema = rs.get('$ref', '').split('/')[-1] or None
            config_schema = None
            if config_loc == 'query':
                for p in params:
                    if p.get('name') == 'CONFIG':
                        config_schema = p.get('schema', {}).get('$ref', '').split('/')[-1] or None
            elif body_props.get('CONFIG'):
                config_schema = body_props['CONFIG'].get('$ref', '').split('/')[-1] or None
            statuscodes = []
            for code, rv in resp.items():
                if isinstance(rv, dict):
                    for sc in rv.get('x-zenesis-statuscodes', []):
                        statuscodes.append((str(sc['name']), sc.get('description', ''), sc.get('resolution', '')))
            throttles = op.get('x-zenesis-security', {}).get('throttles', [])
            sections = []
            for secname, secv in op.get('x-zenesis-sections', {}).items():
                for _, item in sorted(secv.items()):
                    if item.get('type') == 'editor' and item.get('value'):
                        sections.append((secname, html_to_md(item['value'])))
            OPS[mdtitle] = dict(
                title=mdtitle, oas_title=title, operation_id=op['operationId'], method=method.upper(), path=path,
                oasfile=oasfile, domain=dslug, tags=op.get('tags', []), description=op.get('description', '') or op.get('summary', ''),
                scopes=scopes, params=params, req_ct=req_ct, config_loc=config_loc, config_req=config_req,
                body_props=body_props, success=success, resp_ct=resp_ct, resp_schema=resp_schema, config_schema=config_schema,
                statuscodes=statuscodes, throttles=throttles, sections=sections, deprecated=bool(op.get('deprecated')),
                samples=samples.get(path, {}).get(method, {}),
                pointer=f"#/paths/{path.replace('~', '~0').replace('/', '~1')}/{method}",
            )

# --------------------------------------------------------------------------------------------
# Parse markdown docs
# --------------------------------------------------------------------------------------------
def parse_table(block):
    rows = []
    for line in block.split('\n'):
        if line.startswith('|') and not re.match(r'^\|\s*:?-{2,}', line):
            cells = [c.strip() for c in line.strip().strip('|').split(' | ')]
            rows.append(cells)
    return rows

def split_h3(section_text):
    """Return (intro, [(h3 title, body)]) - body keeps its H4+ subsections."""
    parts = re.split(r'(?m)^### (.+)$', section_text)
    intro = parts[0]
    blocks = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    return intro, blocks

def parse_attr_table(intro):
    attrs = collections.OrderedDict()
    for line in intro.split('\n'):
        m = re.match(r'^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$', line)
        if m: attrs[m.group(1).strip()] = m.group(2).strip()
    return attrs

def remove_attr_table(intro):
    out, skipping = [], False
    for line in intro.split('\n'):
        if re.match(r'^\|\s*Attribute\s*\|\s*Value\s*\|', line): skipping = True; continue
        if skipping and line.startswith('|'): continue
        skipping = False
        out.append(line)
    return '\n'.join(out).strip()

def parse_error_rows(block):
    rows = []
    for cells in parse_table(block):
        if len(cells) < 2: continue
        m = re.match(r'^\**\s*(\d{4,6}(?:\s*/\s*\d{4,6})*)\s*\**$', cells[0].replace('`', ''))
        if not m: continue
        codes = re.findall(r'\d{4,6}', m.group(1))
        reason = cells[1] if len(cells) > 1 else ''
        solution = cells[2] if len(cells) > 2 else ''
        for c in codes: rows.append((c, reason, solution))
    return rows

GROUPS = {}   # group slug -> record
ENDPOINTS = []  # ordered endpoint records
APPENDIX_FOUNDATION = {}  # slug of a skipped 'Common HTTP Headers' / 'OAuth Scope Summary' appendix -> foundation path
for dfolder, dslug, dtitle, oasfile, groups in DOMAINS:
    for gfile, gslug, gtitle in groups:
        path = os.path.join(MD_DIR, dfolder, gfile + '.md')
        text = open(path, encoding='utf-8').read()
        h1 = re.search(r'(?m)^# (.+)$', text)
        # H2 sections
        parts = re.split(r'(?m)^## (.+)$', text)
        preamble = parts[0]
        preamble = re.sub(r'(?m)^# .+\n', '', preamble, count=1).strip()
        sections = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
        grp = dict(slug=gslug, title=gtitle, domain=dslug, domain_title=dtitle, mdfile=path, mdname=gfile,
                   h1=h1.group(1) if h1 else gtitle, preamble=preamble, concept_sections=[], endpoints=[],
                   heading_owner={}, anchor_map={}, anchor_title={}, oasfile=oasfile)
        GROUPS[gslug] = grp
        for stitle, body in sections:
            m = re.match(r'^(\d+)\.\s+(.+)$', stitle)
            if m:
                n, etitle = int(m.group(1)), m.group(2).strip()
                intro, blocks = split_h3(body)
                attrs = parse_attr_table(intro)
                ep = dict(n=n, title=etitle, group=gslug, domain=dslug, intro=remove_attr_table(intro), attrs=attrs,
                          blocks=blocks, section_text=body, op=OPS.get(etitle))
                if ep['op'] is None and etitle in MD_ONLY_OPS:
                    ep['op'] = None
                elif ep['op'] is None:
                    print(f'WARN no OAS operation for markdown endpoint: {etitle} ({gfile})', file=sys.stderr)
                grp['endpoints'].append(ep); ENDPOINTS.append(ep)
                for h in re.findall(r'(?m)^#{3,5} (.+)$', body):
                    grp['heading_owner'].setdefault(slugify(h), ('endpoint', n))
                grp['heading_owner'].setdefault(slugify(stitle), ('endpoint', n))
            else:
                if stitle.lower() == 'index':
                    continue
                if re.match(r'^Appendix [A-Z]\b', stitle) and re.search(r'Common HTTP Headers|OAuth Scope Summary', stitle, re.I):
                    APPENDIX_FOUNDATION[slugify(stitle)] = '/foundations/oauth-scopes.md' if 'scope' in stitle.lower() else '/foundations/request-conventions.md'
                    continue
                grp['concept_sections'].append((stitle, body))
                grp['heading_owner'].setdefault(slugify(stitle), ('overview', None))
                grp.setdefault('anchor_map', {})[slugify(stitle)] = overview_anchor(stitle)
                grp.setdefault('anchor_title', {})[overview_anchor(stitle)] = re.sub(r'^Appendix [A-Z]\s*[–:-]\s*', '', stitle)
                for h in re.findall(r'(?m)^#{3,5} (.+)$', body):
                    grp['heading_owner'].setdefault(slugify(h), ('overview', None))

# Attach OAS operations that have no markdown section (none expected, but keep the check)
matched = {ep['title'] for ep in ENDPOINTS}
for t, op in OPS.items():
    if t not in matched:
        print(f'WARN OAS operation without markdown section: {t} ({op["operation_id"]})', file=sys.stderr)

# Endpoint file naming and paths
def ep_opid(ep):
    if ep['op']: return ep['op']['operation_id']
    return MD_ONLY_OPS[ep['title']]

def ep_dir(ep):
    return f"/domains/{ep['domain']}/{ep['group']}"

def ep_path(ep):
    return f"{ep_dir(ep)}/{kebab(ep_opid(ep))}.md"

def sdk_path(ep):
    return f"/sdk-examples/{ep['domain']}/{ep['group']}/{kebab(ep_opid(ep))}.md"

EP_BY_TITLE = {ep['title']: ep for ep in ENDPOINTS}
EP_BY_GROUP_N = {(ep['group'], ep['n']): ep for ep in ENDPOINTS}

# Method / URL for markdown-only endpoints
def ep_method(ep):
    if ep['op']: return ep['op']['method']
    for k in ('Method', 'HTTP Method', 'METHOD'):
        if k in ep['attrs']: return strip_md(ep['attrs'][k]).split()[0].upper()
    return 'GET'

def ep_url(ep):
    if ep['op']: return ep['op']['path']
    u = ep['attrs'].get('URL', '')
    u = re.sub(r'`', '', u).strip()
    return re.sub(r'<([a-z-]+)>', r'{\1}', u)

# --------------------------------------------------------------------------------------------
# Link rewriting
# --------------------------------------------------------------------------------------------
def legacy_group(name):
    stem = re.sub(r'_API_DOC_INFO\.md$', '', name)
    if stem in LEGACY_ALIAS: return LEGACY_ALIAS[stem]
    k = kebab(stem)
    return k if k in GROUPS else None

ANCHOR_ALIASES = {'response-field-reference': 'response-fields', 'response-field-references': 'response-fields',
                  'config-parameter': 'config-parameter', 'sample-response': 'sample-responses', 'sample-request': 'sample-requests',
                  'notes--behaviour': 'notes--behaviour'}
def resolve_anchor(gslug, anchor, current_ep=None):
    """Return bundle-absolute link target for an in-document anchor of group gslug."""
    grp = GROUPS[gslug]
    anchor = re.sub(r'-\d+$', '', anchor) if anchor not in grp['heading_owner'] and re.sub(r'-\d+$', '', anchor) in grp['heading_owner'] else anchor
    m = re.match(r'^(\d+)-', anchor)
    if m:
        ep = EP_BY_GROUP_N.get((gslug, int(m.group(1))))
        if ep: return ep_path(ep)
    if anchor in APPENDIX_FOUNDATION:
        return APPENDIX_FOUNDATION[anchor]
    if anchor.replace('--', '-') in {k.replace('--', '-'): v for k, v in APPENDIX_FOUNDATION.items()}:
        return {k.replace('--', '-'): v for k, v in APPENDIX_FOUNDATION.items()}[anchor.replace('--', '-')]
    owner = grp['heading_owner'].get(anchor)
    if owner:
        kind, n = owner
        if kind == 'overview':
            return f"/domains/{grp['domain']}/{gslug}/overview.md#{grp['anchor_map'].get(anchor, anchor)}"
        ep = EP_BY_GROUP_N.get((gslug, n))
        a = ANCHOR_ALIASES.get(anchor, anchor)
        if current_ep is not None and ep is current_ep:
            return f'#{a}'
        return f'{ep_path(ep)}#{a}'
    return None

UNRESOLVED = collections.Counter()
FOUNDATION_TITLES = {'/foundations/request-conventions.md': 'Request conventions', '/foundations/oauth-scopes.md': 'OAuth scopes'}
def relabel(label, new, gslug):
    """Replace stale labels (legacy file names, 'Appendix X') with the target's title."""
    if re.fullmatch(r'[A-Z_]+\.md', label):
        g = legacy_group(label)
        return GROUPS[g]['title'] if g else label
    if re.fullmatch(r'Appendix [A-Z]', label):
        base, _, anchor = new.partition('#')
        if base in FOUNDATION_TITLES: return FOUNDATION_TITLES[base]
        if anchor:
            for grp in GROUPS.values():
                if grp['anchor_title'].get(anchor) and base.endswith(f"/{grp['slug']}/overview.md"):
                    return grp['anchor_title'][anchor]
        return label
    return label

def rewrite_links(text, gslug, current_ep=None):
    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(('http://', 'https://', 'mailto:')): return m.group(0)
        if target.startswith('#'):
            new = resolve_anchor(gslug, target[1:], current_ep)
            if new is None:
                UNRESOLVED[(gslug, target)] += 1
                return m.group(0)
            return f'[{relabel(label, new, gslug)}]({new})'
        fm = re.match(r'^([A-Za-z_]+\.md)(#(.+))?$', target)
        if fm:
            g = legacy_group(fm.group(1))
            if not g:
                UNRESOLVED[(gslug, target)] += 1
                return m.group(0)
            if fm.group(3):
                new = resolve_anchor(g, fm.group(3))
                if new is None:
                    UNRESOLVED[(gslug, target)] += 1
                    new = f"/domains/{GROUPS[g]['domain']}/{g}/overview.md"
                return f'[{relabel(label, new, gslug)}]({new})'
            return f"[{relabel(label, '', gslug)}](/domains/{GROUPS[g]['domain']}/{g}/overview.md)"
        return m.group(0)
    return re.sub(r'\[([^\]]*)\]\(([^)\s]+)\)', repl, text)

def link_error_codes(text):
    """Turn bare error code mentions inside backticks into catalog links (outside code fences)."""
    out, fence = [], False
    for line in text.split('\n'):
        if line.startswith('```'): fence = not fence
        if not fence and not line.startswith('|'):
            line = re.sub(r'(?<!\[)`(\d{4,6})`(?!\])', lambda m: f'[`{m.group(1)}`](/foundations/error-codes.md#error-{m.group(1)})' if m.group(1) in ALL_CODES else m.group(0), line)
        out.append(line)
    return '\n'.join(out)

# --------------------------------------------------------------------------------------------
# Error code aggregation
# --------------------------------------------------------------------------------------------
ERRORS = collections.defaultdict(lambda: dict(rows=[], oas=[], constants=collections.Counter(), http=collections.Counter(), ops=set()))
for ep in ENDPOINTS:
    opid = ep_opid(ep)
    for name, body in ep['blocks']:
        if slugify(name) in ('error-codes', 'error-code', 'errors'):
            for code, reason, solution in parse_error_rows(body):
                e = ERRORS[code]; e['rows'].append((ep['title'], rewrite_links(reason, ep['group'], None), rewrite_links(solution, ep['group'], None))); e['ops'].add(ep['title'])
                for c in re.findall(r'`([A-Z][A-Z0-9_]{3,})`', reason): e['constants'][c] += 1
    # HTTP status + constants from sample failure responses in the whole section
    for m in re.finditer(r'\*\*HTTP (\d{3})[^\n]*\*\*[^\n]*\n+```json\n(.*?)```', ep['section_text'], re.S):
        status, body = int(m.group(1)), m.group(2)
        for c in re.findall(r'"errorCode":\s*"?(\d+)', body):
            ERRORS[c]['http'][status] += 1
        for s, c in re.findall(r'"summary":\s*"([A-Z][A-Z0-9_]+)"[^}]*?"errorCode":\s*"?(\d+)', body, re.S):
            ERRORS[c]['constants'][s] += 1
    if ep['op']:
        for code, desc, res in ep['op']['statuscodes']:
            e = ERRORS[code]; e['oas'].append((ep['title'], desc, res)); e['ops'].add(ep['title'])
# constants from common examples
for ex in common['components']['examples'].values():
    v = ex.get('value', {})
    if 'data' in v and 'errorCode' in v['data']:
        ERRORS[str(v['data']['errorCode'])]['constants'][v['summary']] += 1
# constants from OAS examples
for doc in OAS.values():
    s = json.dumps(doc)
    for sm, c in re.findall(r'"summary":\s*"([A-Z][A-Z0-9_]+)",\s*"data":\s*\{\s*"errorCode":\s*"?(\d+)', s):
        ERRORS[c]['constants'][sm] += 1
# error messages seen in sample responses (fallback meaning for codes that have no table row)
for ep in ENDPOINTS:
    for c, msg in re.findall(r'"errorCode":\s*"?(\d+)"?,\s*"errorMessage":\s*"((?:[^"\\]|\\.)*)"', ep['section_text']):
        ERRORS[c].setdefault('messages', collections.Counter())[msg] += 1
for doc in OAS.values():
    for c, msg in re.findall(r'"errorCode":\s*"?(\d+)"?,\s*"errorMessage":\s*"((?:[^"\\]|\\.)*)"', json.dumps(doc)):
        ERRORS[c].setdefault('messages', collections.Counter())[msg] += 1
ALL_CODES = set(ERRORS.keys())

CANONICAL = {
 '7005': ('Unexpected error on the Zoho Analytics server while processing an otherwise valid request. Not caused by the request payload.', 'Retry after a short interval. If the error persists, contact Zoho Analytics support quoting the error code and the time of the request.'),
 '7103': ('The organization or workspace addressed by the request does not exist, has been deleted, or is not visible to the caller.', 'Verify the ZANALYTICS-ORGID header and the workspace-id in the request path.'),
 '7104': ('The view (table, report, dashboard, query table) or other named object addressed by the request does not exist in the given workspace.', 'Verify the view-id or the exact, case-sensitive name used in the request.'),
 '7301': ('The request is authenticated, but the user does not hold the role or view permission required for this operation on the requested resource.', 'Ask the workspace or organization administrator to grant the required permission, or call the API as an Account Admin, Organization Admin or Workspace Admin.'),
 '8083': ('The ZANALYTICS-ORGID header is missing from a request that requires it.', 'Send the organization ID in the ZANALYTICS-ORGID header. Obtain it from Get Org List.'),
 '8535': ('The OAuth access token is missing, expired, revoked, or does not carry the scope required by this operation.', 'Regenerate the access token with the required scope (see the endpoint document) and retry.'),
 '8080': ('CONFIG is not valid JSON, was not URL-encoded correctly, contains an unsupported key, or violates a type or length constraint.', 'Stringify and URL-encode the CONFIG object and send only the documented keys with the documented types.'),
}

def error_http(code):
    e = ERRORS[code]
    if e['http']: return e['http'].most_common(1)[0][0], 'observed in sample responses'
    if code in DEFAULT_HTTP: return DEFAULT_HTTP[code], 'typical'
    return 400, 'typical'

def error_meaning(code):
    e = ERRORS[code]
    if code in CANONICAL: return CANONICAL[code][0]
    if e['oas']:
        return collections.Counter(d for _, d, _ in e['oas']).most_common(1)[0][0]
    if e['rows']:
        return collections.Counter(strip_md(re.sub(r'`[A-Z][A-Z0-9_]{3,}`\s*[—–-]\s*', '', x)) for _, x, _ in e['rows']).most_common(1)[0][0]
    if e.get('messages'):
        return 'Server message: "' + e['messages'].most_common(1)[0][0] + '"'
    return 'Documented only through a sample response; see the summary constant.'

def error_resolution(code):
    e = ERRORS[code]
    if code in CANONICAL: return CANONICAL[code][1]
    if e['oas']:
        return collections.Counter(r for _, _, r in e['oas'] if r).most_common(1)[0][0] if any(r for _, _, r in e['oas']) else ''
    if e['rows']:
        c = collections.Counter(strip_md(x) for _, _, x in e['rows'] if x)
        return c.most_common(1)[0][0] if c else ''
    return ''

# --------------------------------------------------------------------------------------------
# Rendering: endpoint documents
# --------------------------------------------------------------------------------------------
def md_source(ep_or_grp_mdfile, doc_path, sid='markdown-doc', title=None):
    mdfile = ep_or_grp_mdfile
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(mdfile), datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    return dict(id=sid, resource=rel(os.path.join(OUT, doc_path.lstrip('/')), mdfile), title=title or os.path.basename(mdfile), author=SOURCE_AUTHOR, last_modified=mtime)

def oas_source(oasfile, sid='openapi-spec'):
    src = os.path.join(OAS_DIR, oasfile)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(src), datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    return dict(id=sid, resource=f'/references/openapi/{oasfile}', title=f'OpenAPI 3 specification - {oasfile}', author=SOURCE_AUTHOR, last_modified=mtime)

def classify_block(name):
    s = slugify(name)
    if s in ('config-parameter', 'config-parameters', 'url-parameters', 'fields-for-config-json', 'sample-values-for-config-parameter', 'query-parameters', 'request-parameters', 'request-body'):
        return 'request'
    if s in ('sample-requests', 'sample-request'): return 'sample-requests'
    if s in ('sample-responses', 'sample-response'): return 'sample-responses'
    if s in ('response-fields', 'response-field-reference', 'response-field-references', 'response-structure'): return 'response-fields'
    if s in ('notes--behaviour', 'notes-and-behaviour', 'notes--behavior', 'notes', 'behaviour', 'behavior', 'special-cases-and-caveats'): return 'notes'
    if s in ('error-codes', 'error-code', 'errors'): return 'errors'
    return 'other'

def split_response_fields(body):
    """Pull '#### Response Field Reference' style sub-blocks out of a sample-responses block."""
    parts = re.split(r'(?m)^#### (Response Field Reference|Response Fields)\s*$', body)
    if len(parts) == 1: return body, None
    main = parts[0]
    fields = ''.join(parts[2::2])
    return main, fields

def norm_org_header(ep):
    v = strip_md(ep['attrs'].get('ZANALYTICS-ORGID Header', ep['attrs'].get('Mandatory Header', ''))).lower()
    if v.startswith('not required') or 'not required' in v[:40]: return 'not-required'
    if v.startswith('optional'): return 'optional'
    if v.startswith('mandatory') or v.startswith('required') or v.startswith('yes'): return 'required'
    if ep['op']:
        names = [p.get('name') for p in ep['op']['params'] if p.get('in') == 'header']
        if 'ZANALYTICS-ORGID' in names:
            req = next(p.get('required', False) for p in ep['op']['params'] if p.get('name') == 'ZANALYTICS-ORGID')
            return 'required' if req else 'optional'
        return 'not-required'
    return 'required'

def config_info(ep):
    op = ep['op']
    if op and op['config_loc'] != 'none':
        return op['config_loc'], op['config_req']
    txt = ' '.join(b for n, b in ep['blocks'] if classify_block(n) == 'request').lower() + ' ' + ep['intro'].lower()
    if 'no config parameter' in txt or 'takes no config' in txt or 'has no config' in txt: return 'none', False
    if 'config is **mandatory**' in txt or 'config is mandatory' in txt:
        return ('query' if ep_method(ep) == 'GET' else 'form'), True
    if 'config is **optional**' in txt or 'config is optional' in txt or 'config parameter is optional' in txt:
        return ('query' if ep_method(ep) == 'GET' else 'form'), False
    return 'none', False

def render_endpoint(ep):
    op = ep['op']; grp = GROUPS[ep['group']]
    path = ep_path(ep); method = ep_method(ep); url = ep_url(ep)
    opid = ep_opid(ep)
    scopes = op['scopes'] if op else re.findall(r'ZohoAnalytics\.[a-z]+\.[a-z]+', ep['attrs'].get('OAuth Scope', ep['attrs'].get('OAUTHSCOPE', '')))
    org_hdr = norm_org_header(ep)
    cfg_loc, cfg_req = config_info(ep)
    success = (op['success'] if op else None) or ('204' if re.search(r'HTTP 204', ep['section_text']) else '200')
    resp_ct = op['resp_ct'] if op else (['application/json'] if success == '200' else [])
    error_codes = sorted({c for c in ERRORS if ep['title'] in ERRORS[c]['ops']}, key=int)
    rate = ep['attrs'].get('Rate Limit')
    throttle = None
    if op and op['throttles']:
        t = op['throttles'][0]
        throttle = f"{t['threshold']} requests per user per {t['duration']} seconds" + (f"; lockout {t['lock-period']} seconds on breach" if t.get('lock-period') else '')
    desc = first_sentence(op['description'] if op else ep['intro'])
    permission = strip_md(ep['attrs'].get('Permission Required', ep['attrs'].get('PERMISSION REQUIRED', '')))
    if not permission.strip():
        # An empty value renders as '-' in the permission matrix, which reads as
        # 'this call needs no permission'. Point at the group's Permission Model instead,
        # and surface the gap so the source document gets fixed.
        MISSING_PERMISSION.append(ep['title'])
        permission = 'See the Permission Model section of this group overview.'

    meta = collections.OrderedDict()
    meta['type'] = 'API Endpoint'
    meta['title'] = ep['title']
    meta['description'] = desc
    meta['resource'] = BASE_URL + url
    meta['tags'] = ['zoho-analytics', 'rest-api-v2', ep['domain'], ep['group'], method.lower()] + sorted({s.split('.')[1] for s in scopes})
    api = collections.OrderedDict()
    api['operation_id'] = opid
    api['method'] = method
    api['path'] = url
    api['domain'] = ep['domain']
    api['group'] = ep['group']
    api['oauth_scopes'] = scopes
    api['org_id_header'] = org_hdr
    api['config_parameter'] = collections.OrderedDict(location=cfg_loc, required=cfg_req)
    if op and op['req_ct']: api['request_content_type'] = op['req_ct']
    api['success_status'] = int(success)
    api['response_content_types'] = resp_ct
    api['permission_required'] = permission
    if rate: api['rate_limit'] = strip_md(rate)
    elif throttle: api['rate_limit'] = throttle
    api['error_codes'] = [int(c) for c in error_codes]
    if op:
        api['openapi'] = collections.OrderedDict(file=f"/references/openapi/{op['oasfile']}", pointer=op['pointer'],
                                                 config_schema=op['config_schema'], response_schema=op['resp_schema'])
    else:
        api['openapi'] = collections.OrderedDict(file=None, pointer=None, note='This endpoint is documented in the markdown reference only; it is absent from the OpenAPI files.')
    if op and op['samples']: api['sdk_examples'] = sdk_path(ep)
    meta['api'] = api
    sources = [oas_source(op['oasfile'])] if op else []
    meta['sources'] = sources
    meta['status'] = 'deprecated' if (op and op['deprecated']) else 'stable'

    L = []
    L.append(frontmatter(meta))
    L.append(f"# Summary\n")
    L.append(f"**{method} `{url}`** - {ep['title']} ({grp['title']} / {grp['domain_title']}).\n")
    L.append(rewrite_links(ep['intro'], ep['group'], ep).strip() + '\n')
    if op and op['description']:
        a = set(re.findall(r'[a-z]{3,}', strip_md(op['description']).lower())); b = set(re.findall(r'[a-z]{3,}', strip_md(ep['intro']).lower()))
        if a and len(a & b) / len(a) < 0.55:
            L.append('\nFrom the OpenAPI specification:\n\n' + op['description'].strip() + '\n')

    # Endpoint facts table
    rows = [('Operation ID', f'`{opid}`'), ('HTTP method', method), ('URL', f'`{url}`'), ('Base URL', f'`{BASE_URL}` (data-center specific, see [Data centers](/foundations/data-centers.md))')]
    rows.append(('OAuth scope', ', '.join(f'[`{s}`](/foundations/oauth-scopes.md#{slugify(s)})' for s in scopes) or 'Not specified'))
    rows.append(('ZANALYTICS-ORGID header', {'required': '**Required**', 'optional': 'Optional', 'not-required': 'Not required (user-scoped API)'}[org_hdr] + (' - ' + ep['attrs']['ZANALYTICS-ORGID Header'].split('—', 1)[-1].strip() if '—' in ep['attrs'].get('ZANALYTICS-ORGID Header', '') else '')))
    rows.append(('Permission required', permission + ' See [Roles & permissions](/foundations/roles-and-permissions.md).'))
    cfg_txt = {'none': 'No CONFIG parameter', 'query': 'JSON object sent as the URL-encoded `CONFIG` query parameter', 'form': 'JSON object sent as the `CONFIG` field of an `application/x-www-form-urlencoded` body', 'multipart': 'JSON object sent as the `CONFIG` part of a `multipart/form-data` body'}[cfg_loc]
    if cfg_loc != 'none': cfg_txt += ' - **mandatory**' if cfg_req else ' - optional'
    rows.append(('CONFIG parameter', cfg_txt))
    if op and op['req_ct']: rows.append(('Request Content-Type', f"`{op['req_ct']}`"))
    rows.append(('Success response', f'HTTP {success}' + (' with no body' if success == '204' else (' - ' + ', '.join(f'`{c}`' for c in resp_ct) if resp_ct else ''))))
    if rate: rows.append(('Rate limit', rate + ' See [Rate limits](/foundations/rate-limits-and-quotas.md).'))
    elif throttle: rows.append(('Rate limit', throttle + '. See [Rate limits](/foundations/rate-limits-and-quotas.md).'))
    for k, v in ep['attrs'].items():
        if k in ('Method', 'HTTP Method', 'METHOD', 'URL', 'OAuth Scope', 'OAUTHSCOPE', 'ZANALYTICS-ORGID Header', 'Mandatory Header', 'Permission Required', 'PERMISSION REQUIRED', 'Rate Limit', 'API NAME', 'DESCRIPTION', 'Success Status', 'CONFIG'): continue
        rows.append((k, v))
    if op:
        rows.append(('OpenAPI', f"[`{op['oasfile']}`](/references/openapi/{op['oasfile']}) - pointer `{op['pointer']}`" + (f"; CONFIG schema `{op['config_schema']}`" if op['config_schema'] else '') + (f"; response schema `{op['resp_schema']}`" if op['resp_schema'] else '')))
    else:
        rows.append(('OpenAPI', 'Not present in the OpenAPI files (markdown reference only).'))
    L.append('\n# Endpoint\n\n' + rewrite_links(md_table(['Attribute', 'Value'], rows), ep['group'], ep) + '\n')

    # Request
    L.append('\n# Request\n')
    L.append('\n## Headers\n')
    hrows = [('`Authorization`', '`Zoho-oauthtoken <access-token>`', 'Required', 'OAuth 2.0 access token carrying ' + (', '.join(f'`{s}`' for s in scopes) if scopes else 'the required scope') + '. See [Authentication](/foundations/authentication.md).')]
    if org_hdr != 'not-required':
        hrows.append(('`ZANALYTICS-ORGID`', '`<org-id>`', 'Required' if org_hdr == 'required' else 'Optional', 'Organization ID. Obtain it from [Get Org List](/domains/organization-management/org-info-and-settings/get-organizations.md). See [Identifiers](/foundations/identifiers.md).'))
    else:
        hrows.append(('`ZANALYTICS-ORGID`', '-', 'Not required', 'This API is user-scoped and works across all organizations of the caller.'))
    if op:
        for p in op['params']:
            if p.get('in') == 'header' and p.get('name') not in ('ZANALYTICS-ORGID',):
                hrows.append((f"`{p['name']}`", '`<org-id>`', 'Required' if p.get('required') else 'Optional', p.get('description', '')))
    if cfg_loc == 'form': hrows.append(('`Content-Type`', '`application/x-www-form-urlencoded`', 'Required', 'The CONFIG JSON is sent as a form field named `CONFIG`.'))
    if cfg_loc == 'multipart': hrows.append(('`Content-Type`', '`multipart/form-data; boundary=...`', 'Required', 'CONFIG and the payload (FILE or DATA) are sent as form parts.'))
    L.append(md_table(['Header', 'Value', 'Required', 'Notes'], hrows) + '\n')
    # Path params
    prows = []
    if op:
        for p in op['params']:
            if p.get('in') == 'path':
                prows.append((f"`{{{p['name']}}}`", p.get('schema', {}).get('type', 'string'), p.get('description', ''), f"[How to obtain](/foundations/identifiers.md#{slugify(p['name'])})"))
    else:
        for name in re.findall(r'\{([a-z-]+)\}', url):
            prows.append((f'`{{{name}}}`', 'string', ID_SOURCES.get(name, ('', []))[0], f'[How to obtain](/foundations/identifiers.md#{slugify(name)})'))
    L.append('\n## Path Parameters\n\n' + (md_table(['Parameter', 'Type', 'Description', 'Source'], prows) if prows else 'This endpoint has no path parameters.') + '\n')
    # CONFIG + request blocks
    req_blocks = [(n, b) for n, b in ep['blocks'] if classify_block(n) == 'request']
    if req_blocks:
        for n, b in req_blocks:
            L.append(f'\n## {n}\n\n' + rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() + '\n')
    else:
        if cfg_loc == 'none':
            L.append('\n## CONFIG Parameters\n\nThis endpoint takes no CONFIG parameter.\n')
        else:
            L.append('\n## CONFIG Parameters\n\nSee the CONFIG schema in the OpenAPI specification referenced in the Endpoint table.\n')
    if op and op['body_props']:
        others = [(k, v) for k, v in op['body_props'].items() if k != 'CONFIG']
        if others:
            L.append('\n## Other Body Parts\n\n' + md_table(['Part', 'Type', 'Description'], [(f'`{k}`', v.get('type', '') + (f" ({v['format']})" if v.get('format') else ''), v.get('description', '')) for k, v in others]) + '\n')
    if op:
        notes = [t for s, t in op['sections'] if s in ('apiRequestParameters', 'apiRequest', 'apiInfo')]
        if notes:
            L.append('\n## Notes from the OpenAPI specification\n\n' + '\n\n'.join(notes) + '\n')

    # Response
    L.append('\n# Response\n')
    if success == '204':
        L.append('\n## Success Response\n\nHTTP `204 No Content`. The response has no body; treat the status code alone as success. Failures still return the JSON error envelope described in [Response envelope](/foundations/response-envelope.md).\n')
    else:
        L.append(f"\n## Success Response\n\nHTTP `{success}`" + (' with content type ' + ', '.join(f'`{c}`' for c in resp_ct) if resp_ct else '') + '. JSON responses use the standard envelope `{ \"status\": \"success\", \"summary\": ..., \"data\": {...} }` described in [Response envelope](/foundations/response-envelope.md).\n')
    resp_field_blocks = [(n, b) for n, b in ep['blocks'] if classify_block(n) == 'response-fields']
    sample_resp_blocks = []
    for n, b in ep['blocks']:
        if classify_block(n) == 'sample-responses':
            main, fields = split_response_fields(b)
            sample_resp_blocks.append((n, main))
            if fields: resp_field_blocks.append(('Response Fields', fields))
    if resp_field_blocks:
        L.append('\n## Response Fields\n\n' + '\n\n'.join(rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() for n, b in resp_field_blocks) + '\n')
    if op:
        notes = [t for s, t in op['sections'] if s in ('apiResponseParameters', 'apiResponseCodes')]
        if notes:
            L.append('\n## Notes from the OpenAPI specification\n\n' + '\n\n'.join(notes) + '\n')

    # Examples
    L.append('\n# Examples\n')
    for n, b in ep['blocks']:
        if classify_block(n) == 'sample-requests':
            L.append(f'\n## Sample Requests\n\n' + rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() + '\n')
    for n, b in sample_resp_blocks:
        L.append(f'\n## Sample Responses\n\n' + rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() + '\n')
    if op and op['samples']:
        L.append(f"\n## SDK Examples\n\nCode samples in {', '.join(LANG_TITLE[l] for l in LANG_FENCE if l in op['samples'])} are in [SDK examples for {ep['title']}]({sdk_path(ep)}). Client construction is described in [SDK clients](/foundations/sdk-clients.md).\n")

    # Notes
    notes_blocks = [(n, b) for n, b in ep['blocks'] if classify_block(n) == 'notes']
    other_blocks = [(n, b) for n, b in ep['blocks'] if classify_block(n) == 'other']
    if notes_blocks or other_blocks:
        L.append('\n# Notes & Behaviour\n')
        for n, b in notes_blocks:
            L.append('\n' + rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() + '\n')
        for n, b in other_blocks:
            L.append(f'\n## {n}\n\n' + rewrite_links(shift_headings(b, -1), ep['group'], ep).strip() + '\n')

    # Error codes (merged)
    L.append('\n# Error Codes\n')
    L.append('\nEvery failure returns HTTP 4xx/5xx with the JSON error envelope; `data.errorCode` carries the code below. Full definitions are in the [Error code catalog](/foundations/error-codes.md).\n')
    erows = []
    seen = set()
    for n, b in ep['blocks']:
        if classify_block(n) == 'errors':
            for code, reason, solution in parse_error_rows(b):
                erows.append((f'[{code}](/foundations/error-codes.md#error-{code})', str(error_http(code)[0]), reason, solution)); seen.add(code)
    if op:
        for code, desc, res in op['statuscodes']:
            if code not in seen:
                erows.append((f'[{code}](/foundations/error-codes.md#error-{code})', str(error_http(code)[0]), desc, res)); seen.add(code)
    for code in ('8535', '7005'):
        if code not in seen:
            erows.append((f'[{code}](/foundations/error-codes.md#error-{code})', str(error_http(code)[0]), CANONICAL[code][0], CANONICAL[code][1])); seen.add(code)
    erows.sort(key=lambda r: int(re.search(r'\d+', r[0]).group()))
    L.append('\n' + rewrite_links(md_table(['Code', 'HTTP', 'Reason', 'Solution'], erows), ep['group'], ep) + '\n')

    # Related
    L.append('\n# Related\n')
    rel_items = [f"- [{grp['title']} overview](/domains/{grp['domain']}/{grp['slug']}/overview.md) - concepts, limits and behaviours shared by this API group.",
                 f"- [{grp['domain_title']}](/domains/{grp['domain']}/overview.md) - the parent API domain.",
                 '- [Request conventions](/foundations/request-conventions.md), [Response envelope](/foundations/response-envelope.md), [Error code catalog](/foundations/error-codes.md).',
                 '- [OAuth scopes](/foundations/oauth-scopes.md), [Roles & permissions](/foundations/roles-and-permissions.md), [Permission matrix](/foundations/permission-matrix.md).']
    sib = [e for e in grp['endpoints'] if e is not ep]
    if sib:
        rel_items.append('- Other endpoints in this group: ' + ', '.join(f"[{e['title']}]({ep_path(e)})" for e in sib) + '.')
    if op and op['samples']:
        rel_items.append(f"- [SDK examples]({sdk_path(ep)}).")
    L.append('\n' + '\n'.join(rel_items) + '\n')

    body = '\n'.join(L)
    body = link_error_codes(body)
    return path, body

# --------------------------------------------------------------------------------------------
# Rendering: SDK example documents
# --------------------------------------------------------------------------------------------
def render_sdk(ep):
    op = ep['op']; grp = GROUPS[ep['group']]
    path = sdk_path(ep)
    langs = [l for l in LANG_FENCE if l in op['samples']]
    meta = collections.OrderedDict()
    meta['type'] = 'SDK Example'
    meta['title'] = f"SDK examples - {ep['title']}"
    meta['description'] = f"Code samples in {len(langs)} languages for {op['method']} {op['path']} ({op['operation_id']})."
    meta['resource'] = BASE_URL + op['path']
    meta['tags'] = ['zoho-analytics', 'sdk', 'code-sample', ep['domain'], ep['group']] + [kebab(LANG_FENCE[l]) for l in langs]
    meta['api'] = collections.OrderedDict(operation_id=op['operation_id'], method=op['method'], path=op['path'], endpoint_doc=ep_path(ep), languages=[LANG_TITLE[l] for l in langs])
    meta['sources'] = [oas_source(op['oasfile']), dict(id='endpoint-doc', resource=ep_path(ep), title=f"Endpoint reference - {ep['title']}")]
    meta['status'] = 'stable'
    L = [frontmatter(meta)]
    L.append(f"# Summary\n\nCode samples for [{ep['title']}]({ep_path(ep)}) (`{op['method']} {op['path']}`). Replace the placeholder client ID, client secret, refresh token, organization ID, workspace ID and view ID values with your own. The SDK client construction pattern for each language is explained in [SDK clients](/foundations/sdk-clients.md).\n")
    L.append('# Examples\n')
    for l in langs:
        snippets = op['samples'][l].get('snippets', [])
        L.append(f'\n## {LANG_TITLE[l]}\n')
        for i, sn in enumerate(snippets):
            if len(snippets) > 1: L.append(f'\nVariant {i + 1}:\n')
            L.append(f"\n```{LANG_FENCE[l]}\n{sn.get('code', '').rstrip()}\n```\n")
    L.append(f"\n# Related\n\n- [{ep['title']}]({ep_path(ep)}) - full endpoint reference.\n- [{grp['title']} overview](/domains/{grp['domain']}/{grp['slug']}/overview.md).\n- [SDK clients](/foundations/sdk-clients.md).\n")
    return path, '\n'.join(L)

# --------------------------------------------------------------------------------------------
# Rendering: group + domain overviews
# --------------------------------------------------------------------------------------------
def endpoints_table(eps, link_sdk=False):
    rows = []
    for e in eps:
        op = e['op']
        scopes = ', '.join(f'`{s}`' for s in (op['scopes'] if op else []))
        succ = (op['success'] if op else '200') or '200'
        rows.append((f"[{e['title']}]({ep_path(e)})", ep_method(e), f'`{ep_url(e)}`', f'`{ep_opid(e)}`', scopes, succ))
    return md_table(['Endpoint', 'Method', 'Path', 'Operation ID', 'OAuth scope', 'Success'], rows)

def render_group_overview(grp):
    path = f"/domains/{grp['domain']}/{grp['slug']}/overview.md"
    doc = OAS[grp['oasfile']]
    tag_desc = ''
    tagnames = collections.Counter(t for e in grp['endpoints'] if e['op'] for t in e['op']['tags'])
    if tagnames:
        tn = tagnames.most_common(1)[0][0]
        tag_desc = next((t.get('description', '') for t in doc.get('tags', []) if t['name'] == tn), '')
    pre = rewrite_links(grp['preamble'], grp['slug'])
    # drop source-authoring remarks that reference internal document names
    pre = re.sub(r'(?s)\nIt follows the same conventions used in `[A-Z_]+\.md`.*?common error codes\.', '', pre)
    meta = collections.OrderedDict()
    meta['type'] = 'API Group'
    meta['title'] = grp['title']
    meta['description'] = first_sentence(tag_desc or pre)
    meta['tags'] = ['zoho-analytics', 'rest-api-v2', grp['domain'], grp['slug'], 'api-group']
    meta['api'] = collections.OrderedDict(domain=grp['domain'], group=grp['slug'], endpoint_count=len(grp['endpoints']),
                                          endpoints=[collections.OrderedDict(operation_id=ep_opid(e), method=ep_method(e), path=ep_url(e), doc=ep_path(e)) for e in grp['endpoints']])
    meta['sources'] = [oas_source(grp['oasfile'])]
    meta['status'] = 'stable'
    L = [frontmatter(meta)]
    L.append(f"# Summary\n\n{pre.strip()}\n")
    if tag_desc and strip_md(tag_desc)[:50] not in strip_md(pre):
        L.append(f'\n{tag_desc.strip()}\n')
    L.append(f"\n# Endpoints\n\n{endpoints_table(grp['endpoints'])}\n\nAll endpoints require the `Authorization: Zoho-oauthtoken <access-token>` header (see [Authentication](/foundations/authentication.md)) and, unless stated otherwise in the endpoint document, the `ZANALYTICS-ORGID` header (see [Request conventions](/foundations/request-conventions.md)).\n")
    for stitle, body in grp['concept_sections']:
        heading = re.sub(r'^Appendix [A-Z]\s*[–:-]\s*', '', stitle)
        L.append(f'\n# {heading}\n\n' + rewrite_links(shift_headings(body, -1), grp['slug']).strip() + '\n')
    # Errors used by this group
    codes = sorted({c for c in ERRORS for e in grp['endpoints'] if e['title'] in ERRORS[c]['ops']}, key=int)
    if codes:
        L.append('\n# Error Codes Used in This Group\n\n' + md_table(['Code', 'HTTP', 'Meaning'], [(f'[{c}](/foundations/error-codes.md#error-{c})', error_http(c)[0], error_meaning(c)) for c in codes]) + '\n')
    L.append(f"\n# Related\n\n- [{grp['domain_title']}](/domains/{grp['domain']}/overview.md) - parent domain.\n- [Foundations](/foundations/index.md) - authentication, conventions, error codes, roles, identifiers.\n- [Endpoint catalog](/endpoint-catalog.md) - every endpoint in one table.\n")
    return path, link_error_codes('\n'.join(L))

def render_domain_overview(dslug, dtitle, oasfile, groups):
    path = f'/domains/{dslug}/overview.md'
    doc = OAS[oasfile]
    grps = [GROUPS[g] for _, g, _ in groups]
    eps = [e for g in grps for e in g['endpoints']]
    meta = collections.OrderedDict()
    meta['type'] = 'API Domain'
    meta['title'] = dtitle
    meta['description'] = first_sentence(doc['info'].get('description', ''))
    meta['tags'] = ['zoho-analytics', 'rest-api-v2', dslug, 'api-domain']
    meta['api'] = collections.OrderedDict(domain=dslug, groups=[collections.OrderedDict(group=g['slug'], title=g['title'], doc=f"/domains/{dslug}/{g['slug']}/overview.md", endpoint_count=len(g['endpoints'])) for g in grps], endpoint_count=len(eps), openapi=f'/references/openapi/{oasfile}')
    meta['sources'] = [oas_source(oasfile)]
    meta['status'] = 'stable'
    L = [frontmatter(meta)]
    L.append(f"# Summary\n\n{doc['info'].get('description', '').strip()}\n")
    L.append('\n# API Groups\n\n' + md_table(['Group', 'Endpoints', 'Description'], [(f"[{g['title']}](/domains/{dslug}/{g['slug']}/overview.md)", len(g['endpoints']), first_sentence(next((t.get('description', '') for t in doc.get('tags', []) if g['endpoints'] and g['endpoints'][0]['op'] and t['name'] in g['endpoints'][0]['op']['tags']), '') or g['preamble'])) for g in grps]) + '\n')
    L.append(f'\n# Endpoints\n\n{endpoints_table(eps)}\n')
    L.append(f"\n# Related\n\n- [All domains](/domains/index.md)\n- [OpenAPI specification for this domain](/references/openapi/{oasfile})\n- [Foundations](/foundations/index.md)\n")
    return path, '\n'.join(L)

# --------------------------------------------------------------------------------------------
# Rendering: generated foundation documents
# --------------------------------------------------------------------------------------------
def gen_meta(type_, title, desc, tags, extra=None, sources=None):
    m = collections.OrderedDict()
    m['type'] = type_; m['title'] = title; m['description'] = desc; m['tags'] = tags
    if extra: m.update(extra)
    m['sources'] = sources or [dict(id='openapi-common', resource='/references/openapi/zoho-analytics-api-common.json', title='Shared OpenAPI components (scopes, error envelope)', author=SOURCE_AUTHOR)]
    m['status'] = 'stable'
    return m

def all_md_sources(doc_path):
    """Bundle-internal derivation edges: the group overviews that hold the shared narrative."""
    return [dict(id=f"group-{g['slug']}", resource=f"/domains/{g['domain']}/{g['slug']}/overview.md", title=f"{g['title']} - group overview") for g in GROUPS.values()]

def render_error_catalog():
    path = '/foundations/error-codes.md'
    codes = sorted(ERRORS, key=int)
    meta = gen_meta('Error Catalog', 'Error code catalog', f'Every documented Zoho Analytics REST API v2 error code ({len(codes)} codes) with its meaning, typical HTTP status, resolution and the operations that raise it.',
                    ['zoho-analytics', 'rest-api-v2', 'errors', 'error-codes', 'troubleshooting'],
                    extra=collections.OrderedDict(error_code_count=len(codes), envelope='{"status":"failure","summary":"<ERROR_CONSTANT>","data":{"errorCode":<int>,"errorMessage":"<text>"}}'),
                    sources=all_md_sources(path) + [oas_source(f) for f in OAS] + [dict(id='openapi-common', resource='/references/openapi/zoho-analytics-api-common.json', title='Shared OpenAPI components', author=SOURCE_AUTHOR)])
    L = [frontmatter(meta)]
    L.append('# Summary\n')
    L.append('''Every failed request returns an HTTP 4xx or 5xx status and a JSON body in the failure envelope (see [Response envelope](/foundations/response-envelope.md)):

```json
{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {
    "errorCode": 7301,
    "errorMessage": "You (<user-name>) do not have the permission to do this operation. "
  }
}
```

How to use this catalog:

- Match on `data.errorCode` (integer), never on `errorMessage` text, which is localized and may change.
- `summary` carries a stable upper-case constant for many codes; the known constants are listed per code below.
- The HTTP status column says "observed" when a documented sample response shows the status, and "typical" when it is inferred from the code family (401 for token errors, 403 for permission errors, 404 for missing objects, 500 for server errors, 400 for everything else).
- The same code can carry an operation-specific meaning; the "Raised by" table lists each documented reason and solution per operation.
- Retry guidance: 5xx and concurrency guards (for example a job or copy already in progress) are retryable after a delay; 4xx codes are not retryable without changing the request.

# Code Families

| Range | Family | Notes |
|---|---|---|
| 6xxx | Organization, user and role management | Membership, roles, portal domains. |
| 7xxx | Metadata, security and modeling | 7103/7104 missing objects, 7301 permission denied, 73xx sharing, 74xx query tables and data lock, 75xx criteria and formula validation, 78xx export/import. |
| 8xxx | Request validation, jobs and platform limits | 80xx invalid CONFIG and parameters, 81xx import/export jobs and limits, 82xx system tags, 85xx OAuth and parameter framework. |
| 9xxx, 12xxx, 14xxx, 15xxx, 18xxx, 70xxx, 101xxx | Feature specific | Localization (9102), white label (12xxx), scheduling and datasource sync (18xxx), AutoML (70xxx), stream tables (101021). |

# Quick Index
''')
    idx = []
    for c in codes:
        e = ERRORS[c]; http, kind = error_http(c)
        const = ', '.join(f'`{k}`' for k, _ in e['constants'].most_common(3)) or '-'
        idx.append((f'[{c}](#error-{c})', const, http, error_meaning(c)[:160], len(e['ops'])))
    L.append('\n' + md_table(['Code', 'Summary constant', 'HTTP', 'Meaning', 'Operations'], idx) + '\n')
    L.append('\n# Codes\n')
    for c in codes:
        e = ERRORS[c]; http, kind = error_http(c)
        L.append(f'\n## Error {c}\n')
        rows = [('Error code', f'`{c}`'), ('Summary constant', ', '.join(f'`{k}`' for k, _ in e['constants'].most_common()) or 'Not documented'),
                ('HTTP status', f'{http} ({kind})'), ('Meaning', error_meaning(c)), ('Resolution', error_resolution(c) or 'See the operation-specific solutions below.'),
                ('Retryable', 'Yes, after a short delay' if http >= 500 or re.search(r'in progress|already running|try again|later', error_meaning(c), re.I) else 'No, fix the request first')]
        L.append('\n' + md_table(['Attribute', 'Value'], rows) + '\n')
        seen = collections.OrderedDict()
        for opt, reason, solution in e['rows']:
            key = strip_md(reason)
            seen.setdefault((key, reason, solution), []).append(opt)
        for opt, desc, res in e['oas']:
            key = strip_md(desc)
            if not any(strip_md(k[1]) == key for k in seen):
                seen.setdefault((key, desc, res), []).append(opt)
            else:
                for k in seen:
                    if strip_md(k[1]) == key and opt not in seen[k]: seen[k].append(opt)
        rr = []
        for (key, reason, solution), opts in seen.items():
            links = ', '.join(f"[{o}]({ep_path(EP_BY_TITLE[o])})" if o in EP_BY_TITLE else o for o in sorted(set(opts)))
            rr.append((links, reason, solution))
        if rr:
            L.append('\nRaised by:\n\n' + md_table(['Operation(s)', 'Reason', 'Solution'], rr) + '\n')
    return path, '\n'.join(L)

def render_error_quick_reference():
    path = '/foundations/error-codes-quick-reference.md'
    codes = sorted(ERRORS, key=int)
    meta = gen_meta('Reference', 'Error codes - quick reference', f'Compact one-line-per-code table of all {len(codes)} Zoho Analytics REST API v2 error codes (code, summary constant, HTTP status, meaning); use the full catalog for per-operation reasons and solutions.',
                    ['zoho-analytics', 'rest-api-v2', 'errors', 'error-codes', 'quick-reference'],
                    extra=collections.OrderedDict(error_code_count=len(codes), full_catalog='/foundations/error-codes.md'),
                    sources=[dict(id='error-catalog', resource='/foundations/error-codes.md', title='Error code catalog (this bundle)', author=SOURCE_AUTHOR)])
    L = [frontmatter(meta), '# Summary\n', f'One row per error code. Follow the code link for the full entry with per-operation reasons, solutions and the operations that raise it. Failure envelope: `{{"status":"failure","summary":"<CONSTANT>","data":{{"errorCode":<int>,"errorMessage":"..."}}}}`. HTTP status is "observed" from documented samples or "typical" for the code family. See [Error code catalog](/foundations/error-codes.md) and [HTTP status codes](/foundations/http-status-codes.md).\n', '# Codes\n']
    rows = []
    for c in codes:
        e = ERRORS[c]; http, kind = error_http(c)
        rows.append((f'[{c}](/foundations/error-codes.md#error-{c})', ', '.join(f'`{k}`' for k, _ in e['constants'].most_common(2)) or '-', f'{http} ({kind[:8]})', error_meaning(c)[:220], len(e['ops'])))
    L.append('\n' + md_table(['Code', 'Constant', 'HTTP', 'Meaning', 'Ops'], rows) + '\n')
    return path, '\n'.join(L)

def render_scopes():
    path = '/foundations/oauth-scopes.md'
    usage = collections.defaultdict(list)
    for e in ENDPOINTS:
        for s in (e['op']['scopes'] if e['op'] else []): usage[s].append(e)
    meta = gen_meta('Reference', 'OAuth scopes', 'All Zoho Analytics OAuth 2.0 scopes, what each family covers, and which REST API v2 operations require each scope.',
                    ['zoho-analytics', 'rest-api-v2', 'oauth', 'scopes', 'authentication'],
                    extra=collections.OrderedDict(scope_count=len(SCOPES), scopes=list(SCOPES.keys())))
    L = [frontmatter(meta)]
    L.append('''# Summary

Zoho Analytics scopes follow the pattern `ZohoAnalytics.<family>.<operation>`. The `<operation>` is one of `read`, `create`, `update`, `delete`, or `all` (every operation of that family). `ZohoAnalytics.fullaccess.all` grants every family. Request only the scopes your integration needs; an access token missing the required scope fails with error [`8535`](/foundations/error-codes.md#error-8535) (`INVALID_OAUTHTOKEN`).

Scopes are requested during the OAuth authorization step (see [Authentication](/foundations/authentication.md)) as a comma-separated `scope` parameter, for example `ZohoAnalytics.data.read,ZohoAnalytics.metadata.read`.

# Scope Families

| Family | Covers |
|---|---|
| `data` | Row data: import, export, add/update/delete rows, sync and refetch. |
| `modeling` | Schema objects: tables, columns, lookups, query tables, formulas, variables. |
| `metadata` | Read-only metadata: organizations, workspaces, views, folders, trash, dependents. |
| `share` | Sharing, publishing, private/public URLs, slideshows, groups, workspace users. |
| `embed` | Embed URLs for Embedded Analytics (OEM) customers. |
| `usermanagement` | Organization users, roles, subscription and resource usage. |
| `fullaccess` | Everything above. |

# Scopes
''')
    rows = []
    for s, d in SCOPES.items():
        rows.append((f'[`{s}`](#{slugify(s)})', d, len(usage.get(s, []))))
    L.append('\n' + md_table(['Scope', 'Description', 'Operations'], rows) + '\n')
    L.append('\n# Operations per Scope\n')
    for s, d in SCOPES.items():
        L.append(f'\n## {s}\n\n{d}\n')
        eps = usage.get(s, [])
        if eps:
            L.append('\n' + md_table(['Operation', 'Method', 'Path'], [(f"[{e['title']}]({ep_path(e)})", ep_method(e), f'`{ep_url(e)}`') for e in eps]) + '\n')
        else:
            L.append('\nNo documented v2 operation declares this scope directly. `.all` scopes satisfy any operation of the same family; `fullaccess.all` satisfies every operation.\n')
    L.append('\n# Related\n\n- [Authentication](/foundations/authentication.md)\n- [Permission matrix](/foundations/permission-matrix.md)\n')
    return path, '\n'.join(L)

def render_rate_limits():
    path = '/foundations/rate-limits-and-quotas.md'
    rows = []
    for e in ENDPOINTS:
        op = e['op']
        if op and op['throttles']:
            t = op['throttles'][0]
            rows.append((f"[{e['title']}]({ep_path(e)})", f"{t['threshold']} requests / user / {t['duration']} s", (f"{t['lock-period'] // 60} minutes" if t.get('lock-period') else '-'), strip_md(e['attrs'].get('Rate Limit', ''))))
        elif e['attrs'].get('Rate Limit'):
            rows.append((f"[{e['title']}]({ep_path(e)})", strip_md(e['attrs']['Rate Limit']), '-', ''))
    meta = gen_meta('Reference', 'Rate limits, throttling and quotas', 'Per-operation request throttles, concurrency guards, plan-governed quotas and API unit consumption for the Zoho Analytics REST API v2.',
                    ['zoho-analytics', 'rest-api-v2', 'rate-limits', 'throttling', 'quotas', 'api-units'], sources=all_md_sources(path) + [oas_source(f) for f in OAS])
    L = [frontmatter(meta)]
    L.append('''# Summary

Three different mechanisms limit how much an integration can do. They are enforced independently and produce different signals.

| Mechanism | Scope | Signal | What to do |
|---|---|---|---|
| **Request throttles** | Specific write-heavy operations (query tables, formulas) | Request rejected for the lock period after the threshold is crossed within the window | Space out calls; on rejection wait for the lock period, do not retry in a tight loop. |
| **Concurrency guards** | One long-running operation per object at a time (workspace copy, table refetch, query table design edit, export/import job slots) | A specific error code such as `18072`, `7429`, `8132` | Wait for the running operation to finish, then retry. Backing off blindly does not help. |
| **Plan quotas** | Organization level, governed by the subscription plan (rows, users, scheduled emails, API units, export jobs...) | Error when the quota is exhausted; visible through [Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md) | Monitor `remaining` values; upgrade the plan or reduce consumption. |

# Per-operation Throttles

Throttles are counted per user. Crossing the threshold inside the window locks the user out of that operation for the lock period.
''')
    L.append('\n' + md_table(['Operation', 'Limit', 'Lockout', 'Documented note'], rows) + '\n')
    L.append('''
Additional documented limits:

- Create Query Table and Edit Query Table are also limited to 15 requests per minute service-wide, in addition to the per-user throttle.
- Copy Workspace allows only one copy operation per organization at a time; a second request while a copy is running is rejected.
- Sync Data and Refetch Data are rate limited per user; a burst of calls is locked out for a short cool-off period. Refetch is additionally guarded by one refetch per table at a time (error `18072`).
- Asynchronous export: at most 5 simultaneous export jobs per organization (error `8132`); jobs and their files are retained for 72 hours from creation.
- Synchronous export: payload ceiling 100 MB; tables above one million rows, dashboards, query tables and live-connect views must use the asynchronous export (error `8133`).
- Synchronous import: maximum file size 20 MB per request.

# API Units

Each API call deducts API units from the organization's plan allowance; the exact cost depends on the operation type. The current allocation, usage and remainder are returned by [Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md) under `resourceName: "apiUnits"` (fractional usage is possible). Single-row APIs (Add Row, Update Row, Delete Row) cost one unit per row, so bulk loading should use the import APIs instead.

# Plan Quotas Visible Through the API

[Get Resource Details](/domains/organization-management/org-info-and-settings/get-resource-details.md) reports allocated, used and remaining values for: `users`, `roUsers`, `workspaces`, `rows`, `queryTables`, `archivedrows`, `scheduledImports`, `scheduledEmails`, `apiUnits`, `scheduledAlerts`, `scheduledSnapshots`, `archiveschedule`, `financeMultiorgImports`, `privateLinks`, `actionsByFlow`. `"Unlimited"` means no cap.

# Related

- [Error code catalog](/foundations/error-codes.md)
- [Asynchronous jobs](/foundations/asynchronous-jobs.md)
''')
    return path, link_error_codes('\n'.join(L))

def render_permission_matrix():
    path = '/foundations/permission-matrix.md'
    rows = []
    for e in ENDPOINTS:
        op = e['op']
        rows.append((f"[{e['title']}]({ep_path(e)})", ep_method(e), ', '.join(f'`{s}`' for s in (op['scopes'] if op else [])), norm_org_header(e), rewrite_links(e['attrs'].get('Permission Required', e['attrs'].get('PERMISSION REQUIRED', '-')), e['group'], e)))
    meta = gen_meta('Reference', 'Permission matrix', 'For every Zoho Analytics REST API v2 operation: the OAuth scope, whether the organization header is needed, and the role or view permission the caller must hold.',
                    ['zoho-analytics', 'rest-api-v2', 'permissions', 'roles', 'authorization', 'criteria'], sources=all_md_sources(path))
    L = [frontmatter(meta)]
    L.append('''# Summary

Authorization has two independent layers. Both must pass:

1. **OAuth scope** on the access token (see [OAuth scopes](/foundations/oauth-scopes.md)). A missing scope fails with `8535`.
2. **Role or permission** of the authenticated user on the organization, workspace or view (see [Roles & permissions](/foundations/roles-and-permissions.md)). A missing permission fails with `7301` (`SECURITY_NOT_PERMITTED`).

The `ZANALYTICS-ORGID` column says whether the organization header is `required`, `optional` or `not-required` for the call.

# Matrix
''')
    L.append('\n' + md_table(['Operation', 'Method', 'OAuth scope', 'ZANALYTICS-ORGID', 'Permission required'], rows) + '\n')
    return path, link_error_codes('\n'.join(L))

def render_identifiers():
    path = '/foundations/identifiers.md'
    params = collections.OrderedDict()
    for doc in OAS.values():
        for k, p in doc.get('components', {}).get('parameters', {}).items():
            params.setdefault(p['name'], p.get('description', ''))
    for e in ENDPOINTS:
        if e['op']:
            for p in e['op']['params']:
                if p.get('in') in ('path', 'header'):
                    params.setdefault(p['name'], p.get('description', ''))
    meta = gen_meta('Reference', 'Identifiers and how to obtain them', 'Every identifier used in Zoho Analytics REST API v2 paths and headers (organization, workspace, view, column, job, schedule and more), its format, and the operations that return it.',
                    ['zoho-analytics', 'rest-api-v2', 'identifiers', 'ids', 'path-parameters'], sources=[oas_source(f) for f in OAS])
    L = [frontmatter(meta)]
    L.append('''# Summary

All identifiers are numeric but are transmitted as **strings** (JSON strings in responses, plain text in URL paths and headers). Treat them as opaque strings; never parse them as 32-bit integers, because view and workspace IDs exceed that range. Identifiers are stable for the lifetime of the object but differ across data centers and environments, so resolve them at runtime rather than hard-coding them. The recommended bootstrap sequence is:

1. Call [Get Org List](/domains/organization-management/org-info-and-settings/get-organizations.md) to obtain `orgId` for the `ZANALYTICS-ORGID` header.
2. Call [Get Meta Details From Name](/domains/organization-management/org-info-and-settings/get-meta-details.md) to resolve a workspace name (and optionally a view name) into `workspaceId` and `viewId`.
3. Use listing APIs (views, columns, folders, groups, schedules...) to obtain the remaining IDs.

# Identifiers
''')
    order = ['ZANALYTICS-ORGID', 'ZANALYTICS-DEST-ORGID', 'workspace-id', 'view-id', 'column-id', 'folder-id', 'group-id', 'job-id', 'datasource-id', 'schedule-id', 'querytable-id', 'formula-id', 'variable-id', 'slide-id', 'analysis-id', 'model-id', 'deployment-id', 'role-id']
    for name in order + [n for n in params if n not in order]:
        desc_oas = params.get(name, '')
        label, srcs = ID_SOURCES.get(name, (desc_oas, []))
        L.append(f'\n## {name}\n')
        where = 'HTTP header' if name.startswith('ZANALYTICS') else 'URL path segment `{' + name + '}`'
        L.append(f'\n- **What it is:** {label or desc_oas}\n- **Where it is sent:** {where}.\n- **OpenAPI description:** {desc_oas or "-"}\n')
        links = [f"[{t}]({ep_path(EP_BY_TITLE[t])})" for t in srcs if t in EP_BY_TITLE]
        if links: L.append(f"- **Obtained from:** {', '.join(links)}.\n")
        users = [e for e in ENDPOINTS if e['op'] and any(p.get('name') == name for p in e['op']['params'])]
        if users: L.append(f"- **Used by:** {len(users)} operations, for example " + ', '.join(f"[{e['title']}]({ep_path(e)})" for e in users[:6]) + ('.' if len(users) <= 6 else ', and others.') + '\n')
    L.append('\n# Related\n\n- [Request conventions](/foundations/request-conventions.md)\n- [Glossary](/foundations/glossary.md)\n')
    return path, '\n'.join(L)

def render_endpoint_catalog():
    path = '/endpoint-catalog.md'
    rows = []
    for _, dslug, dtitle, _, groups in DOMAINS:
        for _, g, _ in groups:
            for e in GROUPS[g]['endpoints']:
                op = e['op']
                rows.append((f"[{e['title']}]({ep_path(e)})", ep_method(e), f'`{ep_url(e)}`', f'`{ep_opid(e)}`', f"[{GROUPS[g]['title']}](/domains/{dslug}/{g}/overview.md)", ', '.join(f'`{s}`' for s in (op['scopes'] if op else [])), (op['success'] if op else '200') or '200', norm_org_header(e)))
    meta = gen_meta('API Catalog', 'Endpoint catalog', f'All {len(ENDPOINTS)} Zoho Analytics REST API v2 endpoints in one table: method, path, operation ID, group, OAuth scope, success status and organization-header requirement.',
                    ['zoho-analytics', 'rest-api-v2', 'catalog', 'endpoints', 'index'],
                    extra=collections.OrderedDict(endpoint_count=len(ENDPOINTS), base_url=BASE_URL, machine_readable='/references/endpoint-catalog.json'),
                    sources=[oas_source(f) for f in OAS] + all_md_sources(path))
    L = [frontmatter(meta)]
    L.append(f'''# Summary

Base URL: `{BASE_URL}` (or the data-center equivalent, see [Data centers](/foundations/data-centers.md)). All paths begin with `/restapi/v2`. Bulk (asynchronous) data operations live under `/restapi/v2/bulk/...`. A machine-readable copy of this table is in [`/references/endpoint-catalog.json`](/references/endpoint-catalog.json).

# Endpoints
''')
    L.append('\n' + md_table(['Endpoint', 'Method', 'Path', 'Operation ID', 'Group', 'OAuth scope', 'Success', 'ORGID header'], rows) + '\n')
    return path, '\n'.join(L)

def bundle_manifest():
    """Machine-readable description of the whole bundle, for tooling that consumes it."""
    return json.dumps(collections.OrderedDict([
        ('name', 'zoho-analytics-rest-api-v2'),
        ('title', 'Zoho Analytics REST API v2'),
        ('description', 'Open Knowledge Format bundle covering every public Zoho Analytics REST API v2 endpoint, the conventions shared by all of them, and their error codes, scopes and permissions.'),
        ('version', BUNDLE_VERSION),
        ('okf_version', OKF_VERSION),
        ('api', collections.OrderedDict([
            ('name', 'Zoho Analytics REST API'), ('version', 'v2'),
            ('base_url', BASE_URL), ('path_prefix', '/restapi/v2'),
            ('auth', 'OAuth 2.0 bearer token in the Authorization header, scheme "Zoho-oauthtoken"'),
        ])),
        ('counts', collections.OrderedDict([
            ('domains', len(DOMAINS)), ('groups', len(GROUPS)), ('endpoints', len(ENDPOINTS)),
            ('error_codes', len(ERRORS)), ('oauth_scopes', len(SCOPES)),
            ('sdk_example_documents', sum(1 for e in ENDPOINTS if e['op'] and e['op']['samples'])),
            ('workflow_playbooks', len([f for f in os.listdir(os.path.join(HAND, 'workflows')) if f.endswith('.md')]) if os.path.isdir(os.path.join(HAND, 'workflows')) else 0),
        ])),
        ('entry_points', collections.OrderedDict([
            ('index', '/index.md'), ('overview', '/overview.md'),
            ('usage_guide', '/how-to-use-this-bundle.md'),
            ('endpoint_catalog_markdown', '/endpoint-catalog.md'),
            ('endpoint_catalog_json', '/references/endpoint-catalog.json'),
            ('foundations', '/foundations/index.md'), ('domains', '/domains/index.md'),
            ('workflows', '/workflows/index.md'), ('sdk_examples', '/sdk-examples/index.md'),
            ('openapi', '/references/openapi/'), ('error_catalog', '/foundations/error-codes.md'),
        ])),
        ('trust', collections.OrderedDict([
            ('tier', 'unverified'),
            ('note', 'Content is derived from the Zoho Analytics API reference documents and OpenAPI specifications. No concept carries a verified entry yet.'),
        ])),
        ('generated', collections.OrderedDict([('by', ACTOR), ('at', NOW)])),
    ]), indent=2, ensure_ascii=False)

def catalog_json():
    items = []
    for e in ENDPOINTS:
        op = e['op']; grp = GROUPS[e['group']]
        cfg_loc, cfg_req = config_info(e)
        items.append(collections.OrderedDict(
            operation_id=ep_opid(e), title=e['title'], method=ep_method(e), path=ep_url(e), domain=e['domain'], domain_title=grp['domain_title'],
            group=e['group'], group_title=grp['title'], oauth_scopes=op['scopes'] if op else [], org_id_header=norm_org_header(e),
            config_parameter=dict(location=cfg_loc, required=cfg_req), request_content_type=op['req_ct'] if op else None,
            success_status=int((op['success'] if op else None) or 200), response_content_types=op['resp_ct'] if op else [],
            permission_required=(strip_md(e['attrs'].get('Permission Required', e['attrs'].get('PERMISSION REQUIRED', '')))
                                 or 'See the Permission Model section of this group overview.'),
            error_codes=sorted({int(c) for c in ERRORS if e['title'] in ERRORS[c]['ops']}),
            doc=ep_path(e), sdk_examples=sdk_path(e) if op and op['samples'] else None,
            openapi=dict(file=f"/references/openapi/{op['oasfile']}", pointer=op['pointer']) if op else None))
    return json.dumps(dict(base_url=BASE_URL, endpoint_count=len(items), endpoints=items), indent=2, ensure_ascii=False)

# --------------------------------------------------------------------------------------------
# Index + log generation
# --------------------------------------------------------------------------------------------
def read_meta(path):
    txt = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    if not m: return {}
    meta = {}
    for line in m.group(1).split('\n'):
        mm = re.match(r'^(title|description|type|okf_version): (.*)$', line)
        if mm:
            v = mm.group(2).strip()
            if v.startswith('"'):
                try: v = json.loads(v)
                except Exception: v = v.strip('"')
            meta[mm.group(1)] = v
    return meta

SLUG_TITLES = {}
SLUG_ORDER = {}
for _i, (_, _d, _dt, _, _groups) in enumerate(DOMAINS):
    SLUG_TITLES[_d] = _dt; SLUG_ORDER[_d] = _i
    for _j, (_, _g, _gt) in enumerate(_groups):
        SLUG_TITLES[_g] = _gt; SLUG_ORDER[_g] = _j
SLUG_TITLES.update({'foundations': 'Foundations', 'domains': 'API domains', 'workflows': 'Workflows', 'sdk-examples': 'SDK examples', 'references': 'References', 'openapi': 'OpenAPI specifications'})

def write_indexes():
    for dirpath, dirnames, filenames in os.walk(OUT):
        if os.path.relpath(dirpath, OUT) == '.': continue
        dirnames.sort(key=lambda d: (SLUG_ORDER.get(d, 999), d))
        mds = sorted(f for f in filenames if f.endswith('.md') and f not in ('index.md', 'log.md'))
        base = os.path.basename(dirpath)
        lines = [f'# {SLUG_TITLES.get(base, base.replace("-", " ").title())}\n']
        if 'overview.md' in mds:
            m = read_meta(os.path.join(dirpath, 'overview.md'))
            lines.append(f"* [{m.get('title', 'Overview')}](overview.md) - {m.get('description', '')}")
            mds.remove('overview.md')
        if mds:
            lines.append('\n# Concepts\n')
            for f in mds:
                m = read_meta(os.path.join(dirpath, f))
                lines.append(f"* [{m.get('title', f)}]({f}) - {m.get('description', '')}")
        if dirnames:
            lines.append('\n# Subdirectories\n')
            for d in dirnames:
                sub = os.path.join(dirpath, d)
                m = read_meta(os.path.join(sub, 'overview.md')) if os.path.exists(os.path.join(sub, 'overview.md')) else {}
                count = sum(1 for _, _, fs in os.walk(sub) for x in fs if x.endswith('.md') and x not in ('index.md', 'log.md'))
                lines.append(f"* [{m.get('title', SLUG_TITLES.get(d, d))}]({d}/index.md) - {m.get('description', f'{count} documents')}")
        others = sorted(f for f in filenames if not f.endswith('.md'))
        if others:
            lines.append('\n# Files\n')
            for f in others: lines.append(f'* [{f}]({f})')
        write(os.path.join(dirpath, 'index.md'), '\n'.join(lines) + '\n')

def write_root_index():
    def entry(p):
        if not os.path.exists(os.path.join(OUT, p.lstrip('/'))): return f'* [{p}]({p.lstrip(chr(47))}) - (pending)'
        m = read_meta(os.path.join(OUT, p.lstrip('/')))
        return f"* [{m.get('title', p)}]({p.lstrip('/')}) - {m.get('description', '')}"
    L = ['---', 'okf_version: "0.2"', '---', '', '# Zoho Analytics REST API v2 - Open Knowledge Format bundle', '',
         'Knowledge bundle covering every public Zoho Analytics REST API v2 endpoint, the conventions shared by all of them, and their error codes, scopes and permissions. Start with the overview, then the foundations, then the domain you need.', '',
         '# Start Here', '', entry('/overview.md'), entry('/endpoint-catalog.md'), entry('/how-to-use-this-bundle.md'), '',
         '# Foundations (shared by every endpoint)', '']
    fdir = os.path.join(OUT, 'foundations')
    for f in (sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []):
        if f.endswith('.md') and f not in ('index.md', 'log.md'): L.append(entry('/foundations/' + f))
    L += ['', '# API Domains', '']
    for _, dslug, dtitle, _, groups in DOMAINS:
        n = sum(len(GROUPS[g]['endpoints']) for _, g, _ in groups)
        L.append(f"* [{dtitle}](domains/{dslug}/index.md) - {n} endpoints in {len(groups)} groups: " + ', '.join(gt for _, _, gt in groups) + '.')
    L += ['', '# Workflows', '']
    wdir = os.path.join(OUT, 'workflows')
    for f in (sorted(os.listdir(wdir)) if os.path.isdir(wdir) else []):
        if f.endswith('.md') and f not in ('index.md', 'log.md'): L.append(entry('/workflows/' + f))
    L += ['', '# SDK Examples', '', f'* [SDK examples](sdk-examples/index.md) - code samples in 9 languages for every OpenAPI-documented endpoint, one document per endpoint.', '',
          '# References', '', '* [OpenAPI specifications](references/openapi/index.md) - the OpenAPI 3 files this bundle was generated from, one per domain plus the shared components file.',
          '* [endpoint-catalog.json](references/endpoint-catalog.json) - machine-readable endpoint catalog for tooling (Postman collections, MCP servers, SDK generators).',
          '* [manifest.json](manifest.json) - bundle name, version, OKF version, counts and entry points.', '',
          '* [llms.txt](llms.txt) - curated entry point for AI agents, with absolute links to every document.', '',
          '# History', '', '* [log.md](log.md) - update log for this bundle.', '']
    write(os.path.join(OUT, 'index.md'), '\n'.join(L))

def write_log():
    date = NOW[:10]
    write(os.path.join(OUT, 'log.md'), f'''# Bundle Update Log

## {date}
* **Creation**: Generated the Zoho Analytics REST API v2 OKF v0.2 bundle from the markdown reference docs, OpenAPI specifications and SDK samples under `{VERSION}/` of the analytics-api repository: {len(ENDPOINTS)} endpoint concepts across {len(DOMAINS)} domains and {len(GROUPS)} groups, {sum(1 for e in ENDPOINTS if e['op'] and e['op']['samples'])} SDK example concepts, an error catalog with {len(ERRORS)} codes, and the shared foundations (authentication, conventions, scopes, roles, identifiers, criteria syntax, asynchronous jobs, rate limits, white label, glossary).
* **Note**: Content is machine-generated from the source documents listed in each concept's `sources`. Add `verified` entries after human review.
''')

def write_llms():
    """Curated entry point for this version's bundle (llmstxt.org convention). Every link is
    absolute under OKF_RAW_BASE so an agent can fetch it directly; the one-line descriptions
    are the documents' own frontmatter descriptions."""
    base = OKF_RAW_BASE.rstrip('/')
    def line(p, title=None, desc=None):
        m = read_meta(os.path.join(OUT, p.lstrip('/')))
        return f"- [{title or m.get('title', p)}]({base}/{p.lstrip('/')}): {desc or m.get('description', '')}"
    sdk = sum(1 for e in ENDPOINTS if e['op'] and e['op']['samples'])
    scopes = len(json.load(open(COMMON, encoding='utf-8'))['components']['securitySchemes']['iam-oauth2-schema']['flows']['authorizationCode']['scopes'])
    wdir = os.path.join(OUT, 'workflows')
    workflows = sorted(f for f in os.listdir(wdir) if f.endswith('.md') and f != 'index.md') if os.path.isdir(wdir) else []
    L = [f'# Zoho Analytics REST API {API_VERSION} - OKF bundle', '',
         f'> Open Knowledge Format (OKF v{OKF_VERSION}) bundle for the Zoho Analytics REST API {API_VERSION}: {len(ENDPOINTS)} endpoints across {len(DOMAINS)} domains, with the conventions, OAuth scopes, roles, identifiers and {len(ERRORS)} error codes they share. Base URL {BASE_URL}, path prefix /restapi/{API_VERSION}, OAuth 2.0 with the Zoho-oauthtoken scheme, structured input in a single JSON parameter named CONFIG.', '',
         f'Read overview.md first, then how-to-use-this-bundle.md for the frontmatter contract and navigation rules. Links inside the bundle are relative to the document that contains them; resolve them against that document\'s URL under {base}. Paths beginning with a slash appear only in frontmatter (resource, sources, api.openapi.file) and are relative to the bundle root, which is {base}. This bundle covers API version {API_VERSION} ({VERSION}); the repository manifest at {REPO_MANIFEST.get("raw_base", "").rstrip("/")}/manifest.json names every available version and the artefacts built for each.', '',
         '## Start here', '',
         line('/overview.md'), line('/how-to-use-this-bundle.md'), line('/endpoint-catalog.md'),
         line('/index.md', 'Bundle index', 'the full table of contents.'), '',
         '## Foundations (rules shared by every call)', '']
    fdir = os.path.join(OUT, 'foundations')
    for f in sorted(os.listdir(fdir)):
        if f.endswith('.md') and f != 'index.md': L.append(line('/foundations/' + f))
    L += ['', '## API domains', '']
    for _, dslug, dtitle, _, groups in DOMAINS:
        L.append(line(f'/domains/{dslug}/overview.md', dtitle))
    L += ['', '## Workflows', '',
          f'- [Workflow playbooks]({base}/workflows/index.md): {len(workflows)} step-by-step procedures spanning several endpoints.']
    for f in workflows: L.append(line('/workflows/' + f))
    L += ['', '## Machine-readable', '',
          f'- [manifest.json]({base}/manifest.json): bundle version, OKF version, counts, entry points.',
          f'- [endpoint-catalog.json]({base}/references/endpoint-catalog.json): every endpoint with method, path, scopes, permission, error codes and document paths.',
          f'- [OpenAPI specifications]({base}/references/openapi/): OpenAPI 3 files, one per domain plus shared components.', '',
          '## Optional', '',
          f'- [SDK examples]({base}/sdk-examples/index.md): per-endpoint code samples ({sdk} documents) in cURL, C#, Go, Java, PHP, Python, Node.js, Ruby and Deluge.',
          line('/foundations/sdk-clients.md', 'SDK clients'),
          f'- [Update log]({base}/log.md): the OKF log for this bundle.', '']
    write(os.path.join(OUT, 'llms.txt'), '\n'.join(L))

# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------
def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    count = 0
    for ep in ENDPOINTS:
        p, body = render_endpoint(ep); write(os.path.join(OUT, p.lstrip('/')), body); count += 1
        if ep['op'] and ep['op']['samples']:
            p, body = render_sdk(ep); write(os.path.join(OUT, p.lstrip('/')), body)
    for grp in GROUPS.values():
        p, body = render_group_overview(grp); write(os.path.join(OUT, p.lstrip('/')), body)
    for _, dslug, dtitle, oasfile, groups in DOMAINS:
        p, body = render_domain_overview(dslug, dtitle, oasfile, groups); write(os.path.join(OUT, p.lstrip('/')), body)
    for fn in (render_error_catalog, render_error_quick_reference, render_scopes, render_rate_limits, render_permission_matrix, render_identifiers, render_endpoint_catalog):
        p, body = fn(); write(os.path.join(OUT, p.lstrip('/')), body)
    # references
    refdir = os.path.join(OUT, 'references', 'openapi'); os.makedirs(refdir, exist_ok=True)
    for f in OAS: shutil.copy(os.path.join(OAS_DIR, f), os.path.join(refdir, f))
    shutil.copy(COMMON, os.path.join(refdir, 'zoho-analytics-api-common.json'))
    write(os.path.join(OUT, 'references', 'endpoint-catalog.json'), catalog_json())
    write(os.path.join(OUT, 'manifest.json'), bundle_manifest())
    # hand-written docs
    for dirpath, _, files in os.walk(HAND):
        for f in files:
            if f == 'README.md': continue   # folder documentation for maintainers, not bundle content
            src = os.path.join(dirpath, f)
            dst = os.path.join(OUT, os.path.relpath(src, HAND))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            txt = open(src, encoding='utf-8').read().replace('{{NOW}}', NOW).replace('{{BUILDER}}', BUILDER)
            # Hand-written concepts bypass frontmatter(); OKF §5.2 still requires generated.by.
            txt = ensure_generated_by(txt)
            write(dst, txt)
    # domains index needs overview docs; sdk-examples dirs too
    write_indexes()
    write_root_index()
    write_log()
    write_llms()
    print(f'endpoints={count} groups={len(GROUPS)} errors={len(ERRORS)} sdk={sum(1 for e in ENDPOINTS if e["op"] and e["op"]["samples"])}')
    if MISSING_PERMISSION:
        print(f'WARN {len(MISSING_PERMISSION)} endpoint(s) have no "Permission Required" in their source '
              f'document; each falls back to a pointer at the group Permission Model. Fix the source:', file=sys.stderr)
        for title in MISSING_PERMISSION: print(f'       {title}', file=sys.stderr)
    if UNRESOLVED:
        print('unresolved links:', file=sys.stderr)
        for (g, t), n in UNRESOLVED.most_common(): print(f'  {n:3} {g}: {t}', file=sys.stderr)

if __name__ == '__main__':
    main()
