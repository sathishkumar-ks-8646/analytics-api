#!/usr/bin/env python3
"""
plan.py - Read one or more input markdown documents that describe Zoho Analytics REST API endpoints
(in any layout: an API team hand-off, a draft reference page, release notes with tables) and work out
what they mean for one API version of this repository: which endpoints are new, which already exist
and what differs, and exactly which files have to change.

    python3 tools/api-agent/plan.py --version v2.0 Dashboard_API.md Visual_API.md
    python3 tools/api-agent/plan.py --version v2.0 input.md --json plan.json

The report is for an AI agent (or a human) about to make the change. It never edits anything.

How endpoints are recognised in the input
  * an index table whose header names an API/name column, a method column and a URL/path column;
  * a heading followed by an attribute table with URL / METHOD rows (`| **URL** | POST https://.../restapi/v2/... |`);
  * any heading whose section contains a `METHOD /restapi/...` line.
  Inside an endpoint's section the script also collects: OAuth scope, permission text, CONFIG field
  tables (first column = field), error-code tables (first column = numeric code), and sample blocks.

How they are matched to this repository
  * by HTTP method and path, with every `{param}` / `<param>` placeholder normalised, against the
    operations in <VERSION>/zenesis-oas/*.json; else by title against `x-zenesis-title` / `summary`.
  * a new endpoint is assigned to the API group whose existing paths share the longest prefix.

Standard library only.
"""
import argparse, collections, glob, json, os, re, sys

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL_DIR))
METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')
PATH_RE = re.compile(r'(/restapi/v\d+(?:\.\d+)?/[^\s`|)"\'<>]*)')
METHOD_PATH_RE = re.compile(r'\b(GET|POST|PUT|DELETE|PATCH)\b[^\n`]{0,80}?(/restapi/v\d+[^\s`|)"\'<>]*)')
SCOPE_RE = re.compile(r'(ZohoAnalytics\.[A-Za-z]+\.[A-Za-z]+)')
CODE_RE = re.compile(r'^\**\s*(\d{4,6})\s*\**$')


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def norm_path(path):
    """`/restapi/v2/workspaces/{WorkspaceID}/dashboards/<dashboard-id>` -> `/restapi/v2/workspaces/{}/dashboards/{}`"""
    path = path.split('?')[0].rstrip('/').rstrip('.')
    path = re.sub(r'https?://[^/]+', '', path)
    return re.sub(r'(\{[^}]*\}|<[^>]*>|:[A-Za-z_]+)', '{}', path)


def param_names(path):
    return re.findall(r'\{([^}]*)\}|<([^>]*)>', path)


def split_cells(line):
    line = line.strip()
    if not (line.startswith('|') and line.endswith('|')):
        return None
    return [c.strip() for c in line.strip('|').split('|')]


def parse_tables(text):
    """Every markdown table in `text` as (header cells, [row cells...])."""
    tables, lines, i = [], text.split('\n'), 0
    while i < len(lines):
        cells = split_cells(lines[i])
        if cells and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-{3,}', lines[i + 1]):
            header, rows, i = cells, [], i + 2
            while i < len(lines):
                r = split_cells(lines[i])
                if r is None:
                    break
                rows.append(r); i += 1
            tables.append((header, rows))
        else:
            i += 1
    return tables


def strip_md(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    return s.replace('**', '').replace('`', '').strip()


# ----------------------------------------------------------------------------- input parsing

class Candidate:
    def __init__(self, title, method, path, source):
        self.title, self.method, self.path, self.source = title.strip(), method.upper(), path.strip(), source
        self.scopes, self.permission, self.description = [], '', ''
        self.config_fields, self.error_codes, self.has_samples = [], [], False
        self.section = ''

    @property
    def key(self):
        return (self.method, norm_path(self.path))

    def to_dict(self):
        return dict(title=self.title, method=self.method, path=self.path, normalized_path=norm_path(self.path),
                    source=self.source, scopes=self.scopes, permission=self.permission, description=self.description,
                    config_fields=self.config_fields, error_codes=self.error_codes, has_samples=self.has_samples)


def sections(text):
    """[(level, heading, body)] for every heading in the document."""
    out, cur = [], None
    for line in text.split('\n'):
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            cur = [len(m.group(1)), m.group(2).strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[2].append(line)
    return [(l, h, '\n'.join(b)) for l, h, b in out]


def clean_title(h):
    h = re.sub(r'^\d+\\?\.\s*', '', h)       # "1\. Create Dashboard" / "1. Create Dashboard"
    return strip_md(h)


def extract(path):
    text = read(path)
    src = os.path.relpath(path, os.getcwd()) if os.path.isabs(path) else path
    found = collections.OrderedDict()

    # 1. attribute tables and METHOD /path lines inside sections
    secs = sections(text)
    for idx, (level, heading, body) in enumerate(secs):
        # body of this section up to the next heading of the same or higher level
        sub = body
        for l2, h2, b2 in secs[idx + 1:]:
            if l2 <= level:
                break
            sub += '\n' + ('#' * l2) + ' ' + h2 + '\n' + b2
        attrs = {}
        for header, rows in parse_tables(body):
            if len(header) >= 2 and header[0].lower() in ('attribute', 'field', 'property', 'item', 'key'):
                for r in rows:
                    if len(r) >= 2:
                        attrs[strip_md(r[0]).lower()] = r[1]
        url_cell = next((v for k, v in attrs.items() if k in ('url', 'endpoint', 'request url')), None)
        method_cell = next((v for k, v in attrs.items() if k in ('method', 'http method', 'httpmethod')), None)
        method, p = None, None
        if url_cell:
            m = METHOD_PATH_RE.search(url_cell) or PATH_RE.search(url_cell)
            if m:
                p = m.group(m.lastindex)
                method = m.group(1) if m.lastindex == 2 else (strip_md(method_cell or '').upper() or None)
        if not p:
            m = METHOD_PATH_RE.search(body)
            if m and re.match(r'^\d+\\?\.\s', heading):
                method, p = m.group(1), m.group(2)
        if not (method and p and method in METHODS):
            continue
        title = next((strip_md(v) for k, v in attrs.items() if k in ('api name', 'name', 'api')), None) or clean_title(heading)
        c = Candidate(title, method, p, f'{src}#{heading}')
        c.section = sub
        c.scopes = sorted(set(SCOPE_RE.findall(next((v for k, v in attrs.items() if 'scope' in k), '') or '')))
        c.permission = strip_md(next((v for k, v in attrs.items() if 'permission' in k), ''))
        c.description = strip_md(next((v for k, v in attrs.items() if k == 'description'), '')) or first_para(body)
        for header, rows in parse_tables(sub):
            h0 = header[0].lower() if header else ''
            if h0 in ('attribute', 'parameter', 'field', 'key', 'name', 'property') and len(header) >= 3 and any('mandatory' in h.lower() or 'required' in h.lower() or 'type' in h.lower() for h in header[1:]):
                for r in rows:
                    f = strip_md(r[0]).strip('.')
                    if f and f not in c.config_fields and not f.lower().startswith(('api name', 'url')):
                        c.config_fields.append(f)
            if h0 in ('code', 'error code', 'errorcode', 'error', 'status code') or 'code' in h0:
                for r in rows:
                    for part in re.split(r'\s*/\s*|,\s*', strip_md(r[0])):
                        mm = CODE_RE.match(part.strip())
                        if mm and int(mm.group(1)) not in c.error_codes:
                            c.error_codes.append(int(mm.group(1)))
        c.has_samples = '```' in sub
        found.setdefault(c.key, c)

    # 2. index tables: anything the sections missed
    for header, rows in parse_tables(text):
        hl = [h.lower() for h in header]
        mi = next((i for i, h in enumerate(hl) if h in ('method', 'http method')), None)
        ui = next((i for i, h in enumerate(hl) if h in ('url', 'path', 'endpoint')), None)
        ni = next((i for i, h in enumerate(hl) if 'api' in h or 'name' in h or 'operation' in h), None)
        if mi is None or ui is None or ni is None:
            continue
        for r in rows:
            if len(r) <= max(mi, ui, ni):
                continue
            method = strip_md(r[mi]).upper()
            m = PATH_RE.search(r[ui])
            if method in METHODS and m:
                c = Candidate(strip_md(r[ni]), method, m.group(1), f'{src}#index')
                found.setdefault(c.key, c)
    return list(found.values())


def first_para(body):
    for para in body.strip().split('\n\n'):
        para = para.strip()
        if para and not para.startswith(('|', '>', '#', '```', '-', '*')):
            return strip_md(para.replace('\n', ' '))
    return ''


# ----------------------------------------------------------------------------- repository state

def deref(doc, obj):
    if isinstance(obj, dict) and '$ref' in obj and str(obj['$ref']).startswith('#/'):
        node = doc
        for part in obj['$ref'][2:].split('/'):
            node = node[part.replace('~1', '/').replace('~0', '~')]
        return node
    return obj


def property_names(doc, schema, seen=None, depth=0):
    """Every property name reachable from a schema (nested objects, arrays, allOf/oneOf, $refs)."""
    seen = seen if seen is not None else set()
    names = set()
    if depth > 12 or not isinstance(schema, dict):
        return names
    ref = schema.get('$ref')
    if ref:
        if ref in seen:
            return names
        seen.add(ref)
    schema = deref(doc, schema)
    for k, v in (schema.get('properties') or {}).items():
        names.add(k)
        names |= property_names(doc, v, seen, depth + 1)
    for key in ('items', 'additionalProperties'):
        if isinstance(schema.get(key), dict):
            names |= property_names(doc, schema[key], seen, depth + 1)
    for key in ('allOf', 'oneOf', 'anyOf'):
        for sub in schema.get(key) or []:
            names |= property_names(doc, sub, seen, depth + 1)
    return names


def config_properties(doc, op):
    rb = op.get('requestBody')
    if rb:
        for media in rb.get('content', {}).values():
            schema = deref(doc, media.get('schema', {}))
            cfg = schema.get('properties', {}).get('CONFIG')
            if cfg is not None:
                return sorted(property_names(doc, cfg))
    for prm in op.get('parameters', []):
        prm = deref(doc, prm)
        if prm.get('name') == 'CONFIG':
            return sorted(property_names(doc, prm.get('schema', {})))
    return []


def status_codes(op):
    codes = set()
    for resp in op.get('responses', {}).values():
        for sc in resp.get('x-zenesis-statuscodes', []) or []:
            try:
                codes.add(int(str(sc.get('name', '')).strip()))
            except ValueError:
                pass
    return codes


class Repo:
    def __init__(self, version):
        self.version = version
        self.vdir = os.path.join(ROOT, version)
        with open(os.path.join(self.vdir, 'manifest.json'), encoding='utf-8') as f:
            self.manifest = json.load(f)
        self.groups = {}          # tag -> dict(folder, md, slug, domain folder, oas file, samples file)
        for d in self.manifest['domains']:
            for g in d['groups']:
                self.groups[g['tag']] = dict(tag=g['tag'], md=f"{version}/md/{d['folder']}/{g['md']}.md",
                                             oas=f"{version}/zenesis-oas/{d['slug']}-grouped-api.json",
                                             samples=f"{version}/zenesis-oas-samples/{d['slug']}-grouped-api-samples.json",
                                             domain=d['folder'], okf=g.get('okf', {}))
        self.ops = {}             # (METHOD, normalized path) -> record
        self.by_title = {}
        for f in sorted(glob.glob(os.path.join(self.vdir, 'zenesis-oas', '*.json'))):
            with open(f, encoding='utf-8') as fh:
                doc = json.load(fh)
            for path, item in doc.get('paths', {}).items():
                for method, op in item.items():
                    if method.upper() not in METHODS:
                        continue
                    scopes = sorted({s for sec in op.get('security', []) for s in sec.get('iam-oauth2-schema', [])})
                    rec = dict(file=f'{version}/zenesis-oas/{os.path.basename(f)}', method=method.upper(), path=path,
                               title=op.get('x-zenesis-title') or op.get('summary'), operation_id=op.get('operationId'),
                               tag=(op.get('tags') or [None])[0], scopes=scopes, config_fields=config_properties(doc, op),
                               error_codes=sorted(status_codes(op)), deprecated=bool(op.get('deprecated')))
                    self.ops[(method.upper(), norm_path(path))] = rec
                    if rec['title']:
                        self.by_title[rec['title'].lower()] = rec
        self.md_titles = {}       # (md file) -> {title: section number}
        for g in self.groups.values():
            p = os.path.join(ROOT, g['md'])
            if os.path.isfile(p):
                self.md_titles[g['md']] = {m.group(2).strip(): int(m.group(1)) for m in re.finditer(r'^## (\d+)\. (.+)$', read(p), re.M)}
        self.samples = {}         # (METHOD, normalized path) -> languages
        for f in sorted(glob.glob(os.path.join(self.vdir, 'zenesis-oas-samples', '*.json'))):
            with open(f, encoding='utf-8') as fh:
                data = json.load(fh)
            for path, methods in data.items():
                for method, langs in methods.items():
                    self.samples[(method.upper(), norm_path(path))] = sorted(langs.keys())

    def suggest_group(self, method, path):
        """The group whose existing paths share the longest prefix with `path`."""
        best, best_len = None, -1
        target = norm_path(path).split('/')
        for rec in self.ops.values():
            parts = norm_path(rec['path']).split('/')
            n = 0
            for a, b in zip(target, parts):
                if a != b:
                    break
                n += 1
            if n > best_len:
                best, best_len = rec['tag'], n
        return best, best_len


# ----------------------------------------------------------------------------- the plan

def analyse(repo, candidates):
    plan = []
    for c in candidates:
        rec = repo.ops.get(c.key) or repo.by_title.get(c.title.lower())
        entry = dict(candidate=c.to_dict())
        if rec is None:
            tag, shared = repo.suggest_group(c.method, c.path)
            g = repo.groups.get(tag, {})
            entry.update(status='NEW', suggested_group=tag, suggested_group_confidence=shared, files=dict(
                md=g.get('md'), zenesis_oas=g.get('oas'), samples=g.get('samples')),
                notes=['no operation with this method and path, and no operation with this title'])
            if g.get('md') in repo.md_titles:
                entry['next_section_number'] = max(repo.md_titles[g['md']].values() or [0]) + 1
        else:
            g = repo.groups.get(rec['tag'], {})
            notes, changes = [], {}
            if (c.method, norm_path(c.path)) != (rec['method'], norm_path(rec['path'])):
                notes.append(f"matched by title only; path in repo is {rec['method']} {rec['path']}")
            if c.title and rec['title'] and c.title.lower() != rec['title'].lower():
                changes['title'] = dict(input=c.title, repo=rec['title'],
                                        note='the markdown `## N. Title` and x-zenesis-title are the join key; rename both or keep the repo title')
            if c.scopes and set(c.scopes) != set(rec['scopes']):
                changes['oauth_scopes'] = dict(input=c.scopes, repo=rec['scopes'])
            new_fields = [f for f in c.config_fields if f not in rec['config_fields']]
            if new_fields and rec['config_fields']:
                changes['config_fields_not_in_schema'] = new_fields
            new_codes = [e for e in c.error_codes if e not in rec['error_codes']]
            if new_codes:
                changes['error_codes_not_in_oas'] = new_codes
            md_file = g.get('md')
            in_md = md_file in repo.md_titles and rec['title'] in repo.md_titles[md_file]
            if not in_md:
                notes.append(f"no `## N. {rec['title']}` section in {md_file}; the OKF build cannot join it")
            entry.update(status='EXISTING', operation_id=rec['operation_id'], group=rec['tag'], repo=dict(
                title=rec['title'], path=rec['path'], scopes=rec['scopes'], config_fields=rec['config_fields'],
                error_codes=rec['error_codes'], deprecated=rec['deprecated'],
                sample_languages=repo.samples.get((rec['method'], norm_path(rec['path'])), [])),
                changes=changes, files=dict(md=md_file, zenesis_oas=rec['file'], samples=g.get('samples')), notes=notes)
        plan.append(entry)
    return plan


def render(repo, plan, inputs):
    L = [f'# Change plan for {repo.version}', '',
         f"Inputs: {', '.join(inputs)}  ",
         f"Endpoints found: {len(plan)} - new: {sum(1 for p in plan if p['status'] == 'NEW')}, "
         f"existing: {sum(1 for p in plan if p['status'] == 'EXISTING')}, "
         f"existing with differences: {sum(1 for p in plan if p['status'] == 'EXISTING' and p['changes'])}", '',
         '| # | Status | Method | Path | Title | Group | What to do |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(plan, 1):
        c = p['candidate']
        if p['status'] == 'NEW':
            todo = f"add to group **{p['suggested_group']}** (shared path depth {p['suggested_group_confidence']}); section `## {p.get('next_section_number', '?')}.`"
            group = p['suggested_group'] or '?'
        else:
            todo = ', '.join(p['changes'].keys()) or 'in step'
            if p['notes']:
                todo += ' · ' + '; '.join(p['notes'])
            group = p['group']
        L.append(f"| {i} | {p['status']} | `{c['method']}` | `{c['path']}` | {c['title']} | {group} | {todo} |")
    L += ['', '## Details', '']
    for i, p in enumerate(plan, 1):
        c = p['candidate']
        L += [f"### {i}. {c['title']} - `{c['method']} {c['path']}` - {p['status']}", '']
        if c['description']:
            L.append(f"> {c['description']}")
            L.append('')
        L.append(f"- Source: `{c['source']}`")
        if c['scopes']:
            L.append(f"- OAuth scope in input: {', '.join('`%s`' % s for s in c['scopes'])}")
        if c['permission']:
            L.append(f"- Permission in input: {c['permission']}")
        if c['config_fields']:
            L.append(f"- CONFIG fields in input ({len(c['config_fields'])}): {', '.join('`%s`' % f for f in c['config_fields'][:30])}{' ...' if len(c['config_fields']) > 30 else ''}")
        if c['error_codes']:
            L.append(f"- Error codes in input ({len(c['error_codes'])}): {', '.join(str(e) for e in c['error_codes'])}")
        L.append(f"- Samples in input: {'yes' if c['has_samples'] else 'no'}")
        if p['status'] == 'EXISTING':
            r = p['repo']
            L.append(f"- In repo: operationId `{p['operation_id']}`, title `{r['title']}`, scopes {', '.join('`%s`' % s for s in r['scopes']) or '-'}, "
                     f"{len(r['config_fields'])} CONFIG fields, {len(r['error_codes'])} error codes in x-zenesis-statuscodes, "
                     f"samples in {len(r['sample_languages'])} languages{', deprecated' if r['deprecated'] else ''}")
            for k, v in p['changes'].items():
                L.append(f"- **{k}**: `{json.dumps(v, ensure_ascii=False)}`")
        for n in p['notes']:
            L.append(f"- Note: {n}")
        L.append('- Files to edit:')
        for k, v in p['files'].items():
            L.append(f"  - {k}: `{v}`")
        L.append('')
    L += ['## Next steps', '',
          '1. For every **NEW** endpoint: `python3 tools/api-agent/scaffold.py --version ' + repo.version +
          ' --title "..." --method ... --path ... --group "<tag>"` prints the three skeletons (markdown section, '
          'OpenAPI operation, SDK samples); fill them from the input and paste them into the files above.',
          '2. For every **EXISTING** endpoint with differences: apply the change in the markdown section, the '
          'OpenAPI operation and the samples together (see tools/okf/agent-guide/04-change-playbooks.md).',
          '3. A new group or domain starts in `' + repo.version + '/manifest.json` (folder, slug, `(md, tag)` pairs, `okf` and `postman` blocks).',
          '4. Add a page URL for each new endpoint title to `tools/postman/api-reference-links.json` once it exists on the docs site.',
          '5. `python3 tools/api-agent/pipeline.py --version ' + repo.version + '` until every stage passes; then review `git diff --stat`.', '']
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+', help='markdown file(s) describing endpoints')
    ap.add_argument('--version', help='API version directory (default: `latest` in manifest.json)')
    ap.add_argument('--json', help='also write the plan as JSON to this path')
    a = ap.parse_args()
    version = a.version or os.environ.get('API_VERSION')
    if not version:
        with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as f:
            version = json.load(f)['latest']
    repo = Repo(version)
    candidates = []
    for path in a.inputs:
        if not os.path.isfile(path):
            sys.exit(f'not a file: {path}')
        candidates.extend(extract(path))
    seen, unique = set(), []
    for c in candidates:
        if c.key not in seen:
            seen.add(c.key); unique.append(c)
    plan = analyse(repo, unique)
    print(render(repo, plan, a.inputs))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(dict(version=version, inputs=a.inputs, endpoints=plan), f, indent=2, ensure_ascii=False)
        print(f'plan written to {a.json}', file=sys.stderr)


if __name__ == '__main__':
    main()
