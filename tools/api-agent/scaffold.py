#!/usr/bin/env python3
"""
scaffold.py - Print the three skeletons a new endpoint needs in this repository, already wired to the
conventions every tool parses: the markdown section, the OpenAPI operation (with its x-zenesis-* keys,
the version's common-file $ref and schema stubs) and the SDK samples entry.

    python3 tools/api-agent/scaffold.py --version v2.0 \\
        --title "Create Dashboard" --method POST \\
        --path "/restapi/v2/workspaces/{workspace-id}/dashboards" \\
        --group "Dashboard" --scope ZohoAnalytics.modeling.create \\
        --config form --success 200

    --group   the OpenAPI tag of the API group (see `tag` in <VERSION>/manifest.json); decides the files
    --config  where CONFIG travels: query (GET), form (POST/PUT/DELETE), multipart (imports), none
    --success 200 (JSON body), 201, or 204 (no body)
    --org     required | optional | none   (ZANALYTICS-ORGID header; default required)
    --write DIR   also write the three skeletons as files into DIR (default: print only)

Nothing is edited in place: paste each skeleton into the file named above it, then fill the TODOs
from the input document. Standard library only.
"""
import argparse, json, os, re, sys

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL_DIR))
LANGS = ['Curl', 'C#', 'Go', 'Java', 'Php', 'Python', 'Node', 'Ruby', 'Deluge']


def camel(title):
    words = re.findall(r'[A-Za-z0-9]+', title)
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:]) if words else 'operation'


def pascal(title):
    return ''.join(w.capitalize() for w in re.findall(r'[A-Za-z0-9]+', title))


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version')
    ap.add_argument('--title', required=True)
    ap.add_argument('--method', required=True, choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    ap.add_argument('--path', required=True)
    ap.add_argument('--group', required=True, help='OpenAPI tag of the API group')
    ap.add_argument('--scope', action='append', default=[], help='OAuth scope (repeatable)')
    ap.add_argument('--config', default=None, choices=['query', 'form', 'multipart', 'none'])
    ap.add_argument('--success', type=int, default=None, choices=[200, 201, 204])
    ap.add_argument('--org', default='required', choices=['required', 'optional', 'none'])
    ap.add_argument('--write', metavar='DIR')
    a = ap.parse_args()

    version = a.version or os.environ.get('API_VERSION') or load(os.path.join(ROOT, 'manifest.json'))['latest']
    manifest = load(os.path.join(ROOT, version, 'manifest.json'))
    group = domain = None
    for d in manifest['domains']:
        for g in d['groups']:
            if g['tag'].lower() == a.group.lower():
                group, domain = g, d
    if group is None:
        tags = sorted(g['tag'] for d in manifest['domains'] for g in d['groups'])
        sys.exit(f'no group with tag {a.group!r} in {version}/manifest.json. Known tags: {", ".join(tags)}\n'
                 f'A new group or domain starts in that manifest (folder, slug, (md, tag) pairs, okf and postman blocks).')

    md_file = f"{version}/md/{domain['folder']}/{group['md']}.md"
    oas_file = f"{version}/zenesis-oas/{domain['slug']}-grouped-api.json"
    samples_file = f"{version}/zenesis-oas-samples/{domain['slug']}-grouped-api-samples.json"
    common_ref = manifest['common_ref']
    oas = load(os.path.join(ROOT, oas_file)) if os.path.isfile(os.path.join(ROOT, oas_file)) else {}
    component_params = set((oas.get('components') or {}).get('parameters', {}).keys())

    method = a.method
    config = a.config or ('query' if method == 'GET' else 'form')
    success = a.success or (200 if method == 'GET' or method == 'POST' else 204)
    op_id = camel(a.title)
    schema_base = pascal(a.title)
    scopes = a.scope or [f"ZohoAnalytics.{'metadata' if method == 'GET' else 'modeling'}.{ {'GET': 'read', 'POST': 'create', 'PUT': 'update', 'DELETE': 'delete', 'PATCH': 'update'}[method] }"]
    path_params = re.findall(r'\{([^}]+)\}', a.path)

    # section number: one past the last `## N.` in the group document
    md_path = os.path.join(ROOT, md_file)
    n = 1
    if os.path.isfile(md_path):
        with open(md_path, encoding='utf-8') as f:
            nums = [int(m) for m in re.findall(r'^## (\d+)\. ', f.read(), re.M)]
        n = (max(nums) + 1) if nums else 1

    # ---- markdown section
    org_row = {'required': '| **ZANALYTICS-ORGID Header** | **Mandatory** - Organization ID that owns the workspace. |',
               'optional': '| **ZANALYTICS-ORGID Header** | Optional - scopes the result to one organization. |',
               'none': '| **ZANALYTICS-ORGID Header** | Not required. |'}[a.org]
    config_block = '' if config == 'none' else f'''
### CONFIG Parameters

CONFIG is **mandatory** for this API. <!-- or: optional -->

| Parameter | Type | Mandatory | Default | Description |
|-----------|------|-----------|---------|-------------|
| `TODO` | String | **Yes** | - | TODO |
'''
    sample_request = (f'''GET {a.path.replace('{', '<').replace('}', '>')}?CONFIG=%7B%22TODO%22%3A%22TODO%22%7D HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456''' if config == 'query' else f'''{method} {a.path.replace('{', '<').replace('}', '>')} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456
Content-Type: {'multipart/form-data; boundary=----boundary' if config == 'multipart' else 'application/x-www-form-urlencoded'}

CONFIG={{"TODO":"TODO"}}''') if config != 'none' else f'''{method} {a.path.replace('{', '<').replace('}', '>')} HTTP/1.1
Host: analyticsapi.zoho.com
Authorization: Zoho-oauthtoken 1000.xxxxxx.yyyyyy
ZANALYTICS-ORGID: 700000123456'''
    success_sample = ('**HTTP 204 No Content - Success**\n\nNo response body.' if success == 204 else
                      f'**HTTP {success} OK - Success (Case 1)**\n\n```json\n{{\n  "status": "success",\n  "summary": "{a.title}",\n  "data": {{\n    "TODO": "TODO"\n  }}\n}}\n```')
    md = f'''## {n}. {a.title}

TODO: one or two paragraphs describing what the endpoint does and when to use it.

| Attribute | Value |
|-----------|-------|
| **API NAME** | {a.title} |
| **URL** | `{method} https://<ZohoAnalytics_Server_URI>{a.path.replace('{', '<').replace('}', '>')}` |
| **METHOD** | {method} |
| **OAuth Scope** | {', '.join('`%s`' % s for s in scopes)} |
{org_row}
| **Permission Required** | TODO: who may call it (for example: The authenticated user must be an Account Admin or Organization Admin, or a Workspace Admin, or any user with TODO permission on the workspace). |
{config_block}
### Sample Requests

**Case 1 - TODO: what this case shows**

```http
{sample_request}
```

### Sample Responses

{success_sample}

**HTTP 403 Forbidden - Caller lacks permission**

```json
{{
  "status": "failure",
  "summary": "SECURITY_NOT_PERMITTED",
  "data": {{ "errorCode": 7301, "errorMessage": "TODO" }}
}}
```
{'' if success == 204 else '''
### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data.TODO` | String | TODO |
'''}
### Notes & Behaviour

| Aspect | Detail |
|--------|--------|
| **TODO** | TODO |

### Error Codes

| Code | Reason | Solution |
|------|--------|----------|
| 7301 | `SECURITY_NOT_PERMITTED` - Caller lacks the required permission. | TODO |
| 8535 | Invalid or expired OAuth token. | Provide a valid token with scope {', '.join('`%s`' % s for s in scopes)}. |
'''

    # ---- OpenAPI operation
    parameters = []
    if a.org != 'none':
        parameters.append({'$ref': '#/components/parameters/org-id'} if 'org-id' in component_params else
                          {'name': 'ZANALYTICS-ORGID', 'in': 'header', 'required': a.org == 'required', 'schema': {'type': 'string'},
                           'description': 'Organization ID that owns the workspace.'})
    for p in path_params:
        parameters.append({'$ref': f'#/components/parameters/{p}'} if p in component_params else
                          {'name': p, 'in': 'path', 'required': True, 'schema': {'type': 'string'}, 'description': f'TODO: what {p} identifies and which API returns it.'})
    op = {
        'tags': [group['tag']],
        'x-zenesis-title': a.title,
        'summary': a.title,
        'description': 'TODO: the same first paragraph as the markdown section.\n\nTODO: the permission sentence.',
        'operationId': op_id,
        'x-zenesis-sections': {},
        'parameters': parameters,
    }
    if config == 'query':
        op['parameters'].append({
            'name': 'CONFIG', 'in': 'query', 'required': True, 'style': 'form', 'explode': False,
            'description': 'TODO: what CONFIG controls.\n\nAs this is a GET request, the value must be stringified and URL encoded before it is sent.',
            'schema': {'$ref': f'#/components/schemas/{schema_base}Config'},
            'examples': {'default': {'summary': 'TODO short label', 'description': 'TODO: what this example shows.', 'value': {'TODO': 'TODO'}}},
        })
    elif config in ('form', 'multipart'):
        ct = 'multipart/form-data' if config == 'multipart' else 'application/x-www-form-urlencoded'
        props = {'CONFIG': {'$ref': f'#/components/schemas/{schema_base}Config'}}
        if config == 'multipart':
            props['FILE'] = {'type': 'string', 'format': 'binary', 'description': 'TODO: the file to upload.'}
        op['requestBody'] = {
            'required': True,
            'content': {ct: {
                'schema': {'type': 'object', 'properties': props, 'required': ['CONFIG']},
                'encoding': {'CONFIG': {'contentType': 'application/json'}},
                'examples': {'default': {'summary': 'TODO short label', 'description': 'TODO: what this example shows.', 'value': {'CONFIG': {'TODO': 'TODO'}}}},
            }},
        }
    op['security'] = [{'iam-oauth2-schema': scopes}]
    success_resp = {'description': 'TODO: what a successful response carries.', 'x-zenesis-statuscodes': [
        {'name': '7301', 'description': 'TODO: why 7301 is raised here.', 'resolution': 'TODO'},
        {'name': '8535', 'description': 'Invalid OAuth token.', 'resolution': 'Provide a valid, non-expired OAuth token in the Authorization header.'},
    ]}
    if success != 204:
        success_resp['content'] = {'application/json': {'schema': {'$ref': f'#/components/schemas/{schema_base}Response'}}}
    op['responses'] = {
        str(success): success_resp,
        '4XX': {'$ref': f'{common_ref}#/components/responses/CommonErrorResponse'},
        '500': {'$ref': f'{common_ref}#/components/responses/UnexpectedErrorResponse'},
    }
    schemas = {}
    if config != 'none':
        schemas[f'{schema_base}Config'] = {'type': 'object', 'description': 'TODO', 'properties': {'TODO': {'type': 'string', 'description': 'TODO'}}, 'required': ['TODO']}
    if success != 204:
        schemas[f'{schema_base}Response'] = {'type': 'object', 'properties': {
            'status': {'type': 'string', 'enum': ['success']}, 'summary': {'type': 'string'},
            'data': {'type': 'object', 'properties': {'TODO': {'type': 'string', 'description': 'TODO'}}}}}

    # ---- samples
    curl = (f'curl "https://analyticsapi.zoho.com{a.path}?CONFIG=%7B%22TODO%22%3A%22TODO%22%7D" -H "Authorization: Zoho-oauthtoken <access-token>" -H "ZANALYTICS-ORGID: <org-id>"' if config == 'query' else
            f'curl -X {method} "https://analyticsapi.zoho.com{a.path}" -H "Authorization: Zoho-oauthtoken <access-token>" -H "ZANALYTICS-ORGID: <org-id>"' + ('' if config == 'none' else (' -F \'CONFIG={"TODO":"TODO"}\'' + (' -F "FILE=@/path/to/file.csv"' if config == 'multipart' else '') if config == 'multipart' else ' --data-urlencode \'CONFIG={"TODO":"TODO"}\'')))
    samples = {a.path: {method.lower(): {lang: {'snippets': [{'code': curl if lang == 'Curl' else f'// TODO: {lang} snippet for {a.title}'}]} for lang in LANGS}}}

    out = [
        (f'{md_file}  (append as section {n}; add the row to the `## Index` table)', md, 'section.md'),
        (f'{oas_file}  (paths["{a.path}"]["{method.lower()}"]; schemas go under components.schemas)',
         json.dumps({'paths': {a.path: {method.lower(): op}}, 'components': {'schemas': schemas}}, indent=2, ensure_ascii=False), 'operation.json'),
        (f'{samples_file}  (merge the path key; keys must match the OpenAPI path template and lower-case method exactly)',
         json.dumps(samples, indent=2, ensure_ascii=False), 'samples.json'),
    ]
    for target, text, fname in out:
        print('=' * 100)
        print('PASTE INTO  ' + target)
        print('=' * 100)
        print(text)
        print()
        if a.write:
            os.makedirs(a.write, exist_ok=True)
            with open(os.path.join(a.write, fname), 'w', encoding='utf-8') as f:
                f.write(text if text.endswith('\n') else text + '\n')
    print('Then: fill every TODO from the input, keep `## N. Title` == x-zenesis-title, and run '
          f'python3 tools/api-agent/pipeline.py --version {version}')
    if a.write:
        print(f'(skeletons also written to {a.write}/)')


if __name__ == '__main__':
    main()
