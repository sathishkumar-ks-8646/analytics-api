#!/usr/bin/env python3
"""
package_okf.py - Assemble the public distribution of the Zoho Analytics OKF bundles.

The bundles themselves live in this repository at <VERSION>/okf/ and are consumed from there.
This script exists for one reason: publishing the same bundles to a standalone repository
(zoho/analytics-okf) whose layout is "one top-level directory per API version plus a version
index at the root". It produces a self-contained, git-ready directory:

    dist/analytics-okf/
      README.md            human landing page           (tools/okf/publish/README.md, counts filled in)
      llms.txt             AI/agent entry point         (generated: names every version, links the latest)
      manifest.json        version index                (generated from every <VERSION>/okf/manifest.json)
      CHANGELOG.md         version history              (tools/okf/publish/CHANGELOG.md, verbatim)
      LICENSE.md           licence terms                (tools/okf/publish/LICENSE.md, verbatim)
      tools/validate.py    conformance + link validator (copy of tools/okf/validate_okf.py)
      .github/workflows/validate-okf.yml
      v2.0/                THE BUNDLE for v2.0          (copy of v2.0/okf/, llms.txt links rebased)
      v3.0/                ... one directory per version listed in <repo>/manifest.json

Usage:
    python3 tools/okf/package_okf.py                       # every version in <repo>/manifest.json
    python3 tools/okf/package_okf.py --versions v2.0       # a subset
    python3 tools/okf/package_okf.py --tarball             # also write dist/analytics-okf-<latest bundle version>.tar.gz
    python3 tools/okf/package_okf.py --repo-url https://github.com/zoho/analytics-okf --ref main

Nothing here touches git remotes or pushes. Review the output, then push it yourself.
Re-packaging preserves dist/analytics-okf/.git, so commit history survives.
"""
import argparse, json, os, re, shutil, subprocess, sys, tarfile

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL_DIR))
DIST = os.path.join(ROOT, 'dist')
REPO_NAME = 'analytics-okf'
PUBLISH_TEMPLATES = os.path.join(TOOL_DIR, 'publish')

DEFAULT_REPO = 'https://github.com/zoho/analytics-okf'
DEFAULT_DOCS = 'https://www.zoho.com/analytics/api/v2/'

WORKFLOW = """name: Validate OKF bundle

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Validate OKF conformance and links
        run: |
          shopt -s failglob
          for bundle in v[0-9]*/; do
            echo "::group::validate ${bundle%/}"
            python3 tools/validate.py "${bundle%/}"
            echo "::endgroup::"
          done
      - name: Check machine-readable files parse
        run: |
          shopt -s failglob
          python3 -c "import json;json.load(open('manifest.json'))"
          for f in v[0-9]*/manifest.json v[0-9]*/references/endpoint-catalog.json v[0-9]*/references/openapi/*.json; do
            python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$f"
          done
"""

GITIGNORE = """.DS_Store
__pycache__/
*.pyc
"""


def raw_base(repo_url, ref='main'):
    """Raw-file base URL for a GitHub repo, which is what agents fetch."""
    if 'github.com/' in repo_url:
        owner_repo = repo_url.split('github.com/', 1)[1].strip('/')
        return 'https://raw.githubusercontent.com/' + owner_repo + '/' + ref
    return repo_url.rstrip('/')


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text if text.endswith('\n') else text + '\n')


def version_index(entries, raw, latest):
    """The root manifest.json of the published repository: one entry per bundle."""
    versions = []
    for e in entries:
        m = e['bundle_manifest']
        versions.append({
            'version': e['version'],
            'api_version': m['api']['version'],
            'bundle_version': m['version'],
            'okf_version': m['okf_version'],
            'status': 'stable' if e['status'] == 'current' else e['status'],
            'deprecated_on': e.get('deprecated_on'),
            'sunset_on': e.get('sunset_on'),
            'superseded_by': e.get('superseded_by'),
            'path': e['version'],
            'manifest': f"{e['version']}/manifest.json",
            'index': f"{e['version']}/index.md",
            'entry': f"{e['version']}/llms.txt",
            'endpoint_catalog_json': f"{e['version']}/references/endpoint-catalog.json",
            'api_reference': e.get('api_reference'),
        })
    return {
        'schema_version': '1.1',
        'bundle': 'zoho-analytics-okf',
        'title': 'Zoho Analytics REST API - Open Knowledge Format bundles',
        'description': 'Version index for the Zoho Analytics REST API OKF bundles. One entry per API version; each entry points at that version\'s OKF bundle root and manifest.',
        'okf_spec': 'https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md',
        'raw_base': raw + '/',
        'latest': latest,
        'latest_path': latest,
        'resolution': 'Resolve `latest` against `versions[].version` to find the recommended bundle, or join `raw_base` with `latest_path`. Do not hard-code a version directory: `latest` moves when a newer API version ships, while every published version directory stays where it is, forever.',
        'status_vocabulary': {
            'beta': 'Published for early access. Content may change without a major bundle version bump.',
            'stable': 'Ready for production use and actively maintained.',
            'deprecated': 'Still served and still correct, but superseded. Migrate to `superseded_by` before `sunset_on`.',
            'sunset': 'No longer maintained. Retained for link stability and history only.',
        },
        'versions': versions,
        'note': 'A new API version is added as an additional entry with its own top-level directory; no existing entry or path changes. When that happens, `latest` and `latest_path` move to the new version, and the superseded entry gains `status: deprecated`, a `deprecated_on` date, a `sunset_on` date and a `superseded_by` pointer.',
    }


def root_llms(entries, raw, latest):
    lines = ['# Zoho Analytics REST API - OKF bundles', '',
             '> Version index for the Zoho Analytics REST API Open Knowledge Format bundles. Each API version ships as a self-contained OKF v0.2 bundle in its own top-level directory of this repository. Start with the version you need; every version has its own llms.txt carrying the full link list for that version.', '',
             'Unless the caller has pinned a version, use the newest stable one. It is named by `latest` in',
             f'[manifest.json]({raw}/manifest.json),',
             'which is the only file in this repository whose meaning changes when a new API version ships. Every',
             'published version directory keeps its path forever, so a URL you have already resolved stays valid.',
             f'Today `latest` is **{latest}**; a newer version will appear as a sibling directory and a new entry, and',
             f'nothing under `/{latest}/` will move.', '',
             '## Available versions', '']
    for e in entries:
        m, c = e['bundle_manifest'], e['bundle_manifest']['counts']
        status = 'latest, stable' if e['version'] == latest else ('stable' if e['status'] == 'current' else e['status'])
        lines.append(f"- [{e['version']} ({status})]({raw}/{e['version']}/llms.txt): {c['endpoints']} endpoints across {c['domains']} domains and {c['groups']} groups, {c['error_codes']} error codes, {c['oauth_scopes']} OAuth scopes, {c['workflow_playbooks']} workflow playbooks. Base URL {m['api']['base_url']}, path prefix {m['api']['path_prefix']}, OAuth 2.0 with the Zoho-oauthtoken scheme.")
    lines += ['', '## Machine-readable version index', '',
              f'- [manifest.json]({raw}/manifest.json): every available version with its status, path, lifecycle dates and bundle manifest, plus `latest`. Read this instead of hard-coding a version directory.', '',
              f'## Quick links ({latest})', '',
              f'- [Bundle index]({raw}/{latest}/index.md): the full table of contents.',
              f'- [Overview]({raw}/{latest}/overview.md): what the API is, the object model, and the five conventions every call shares.',
              f'- [How to use this bundle]({raw}/{latest}/how-to-use-this-bundle.md): directory layout, the api frontmatter contract, navigation rules for agents and generators.',
              f'- [Endpoint catalog]({raw}/{latest}/endpoint-catalog.md): every endpoint with method, path, operation ID, group, scope and success status.',
              f'- [Endpoint catalog (JSON)]({raw}/{latest}/references/endpoint-catalog.json): every endpoint, machine-readable.',
              f'- [Bundle manifest]({raw}/{latest}/manifest.json): bundle version, OKF version, counts and entry points.', '',
              '## Optional', '',
              f'- [Changelog]({raw}/CHANGELOG.md): bundle version history across all API versions.',
              f'- [Licence]({raw}/LICENSE.md)', '']
    return '\n'.join(lines)


def rebase_llms(text, old_base, new_base):
    """The per-version llms.txt was written for this repository's raw base; point it at the public one."""
    return text.replace(old_base.rstrip('/'), new_base.rstrip('/'))


def fill_readme(template, entries, latest):
    """The README template carries {{latest}} and {{counts.<key>}} placeholders for the latest bundle."""
    m = next(e for e in entries if e['version'] == latest)['bundle_manifest']
    out = template.replace('{{latest}}', latest).replace('{{bundle_version}}', m['version']).replace('{{okf_version}}', m['okf_version'])
    for k, v in m['counts'].items():
        out = out.replace('{{counts.%s}}' % k, str(v))
    rows = []
    for e in entries:
        c = e['bundle_manifest']['counts']
        status = 'stable' if e['status'] == 'current' else e['status']
        rows.append(f"| [`{e['version']}/`]({e['version']}/index.md) | {e['bundle_manifest']['api']['version']} | {e['bundle_manifest']['version']} | {status} | {c['endpoints']} endpoints, {c['domains']} domains, {c['groups']} groups, {c['error_codes']} error codes |")
    return out.replace('{{versions_table_rows}}', '\n'.join(rows))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--versions', nargs='*', help='version directories to package (default: every version in <repo>/manifest.json)')
    ap.add_argument('--repo-url', default=DEFAULT_REPO, help='public repository URL (default %(default)s)')
    ap.add_argument('--ref', default='main', help='git ref used to build raw file URLs')
    ap.add_argument('--base-url', help='override the raw-file base URL derived from --repo-url/--ref')
    ap.add_argument('--out', default=DIST, help='output directory (default <repo>/dist)')
    ap.add_argument('--tarball', action='store_true', help='also write a .tar.gz next to the directory')
    a = ap.parse_args()

    with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as f:
        repo_manifest = json.load(f)
    wanted = a.versions or [v['version'] for v in repo_manifest['versions']]
    entries = []
    for v in repo_manifest['versions']:
        if v['version'] not in wanted:
            continue
        bundle = os.path.join(ROOT, v['version'], 'okf')
        mf = os.path.join(bundle, 'manifest.json')
        if not os.path.isfile(mf):
            sys.exit(f'bundle not found: {bundle}\nRun: python3 tools/okf/build_okf.py --version {v["version"]}')
        with open(mf, encoding='utf-8') as f:
            e = dict(v); e['bundle_dir'] = bundle; e['bundle_manifest'] = json.load(f); entries.append(e)
    if not entries:
        sys.exit('nothing to package: no listed version matched ' + repr(wanted))
    latest = repo_manifest['latest'] if repo_manifest['latest'] in wanted else entries[-1]['version']
    raw = a.base_url or raw_base(a.repo_url, a.ref)
    this_raw = repo_manifest.get('raw_base', '').rstrip('/')

    out = os.path.join(a.out, REPO_NAME)
    git_dir = os.path.join(out, '.git')
    saved_git = None
    if os.path.isdir(out):
        if os.path.isdir(git_dir):                       # preserve history across re-packaging
            saved_git = os.path.join(a.out, '.git-saved')
            shutil.rmtree(saved_git, ignore_errors=True)
            shutil.move(git_dir, saved_git)
        shutil.rmtree(out)
    os.makedirs(out)
    if saved_git:
        shutil.move(saved_git, git_dir)

    for e in entries:
        dst = os.path.join(out, e['version'])
        shutil.copytree(e['bundle_dir'], dst)
        llms = os.path.join(dst, 'llms.txt')
        if os.path.isfile(llms) and this_raw:
            write(llms, rebase_llms(read(llms), this_raw + '/' + e['version'] + '/okf', raw + '/' + e['version']))

    write(os.path.join(out, 'manifest.json'), json.dumps(version_index(entries, raw, latest), indent=2, ensure_ascii=False))
    write(os.path.join(out, 'llms.txt'), root_llms(entries, raw, latest))
    write(os.path.join(out, 'README.md'), fill_readme(read(os.path.join(PUBLISH_TEMPLATES, 'README.md')), entries, latest))
    for name in ('CHANGELOG.md', 'LICENSE.md'):
        shutil.copy(os.path.join(PUBLISH_TEMPLATES, name), os.path.join(out, name))
    write(os.path.join(out, '.gitignore'), GITIGNORE)
    write(os.path.join(out, '.github', 'workflows', 'validate-okf.yml'), WORKFLOW)
    os.makedirs(os.path.join(out, 'tools'), exist_ok=True)
    shutil.copy(os.path.join(TOOL_DIR, 'validate_okf.py'), os.path.join(out, 'tools', 'validate.py'))

    for e in entries:
        r = subprocess.run([sys.executable, os.path.join(out, 'tools', 'validate.py'), e['version']], cwd=out,
                           capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip())
        if r.returncode:
            sys.exit(f'validation failed for {e["version"]}; not packaging further')

    if a.tarball:
        bv = next(e for e in entries if e['version'] == latest)['bundle_manifest']['version']
        tgz = os.path.join(a.out, f'{REPO_NAME}-{bv}.tar.gz')
        with tarfile.open(tgz, 'w:gz') as tar:
            tar.add(out, arcname=REPO_NAME, filter=lambda ti: None if '/.git' in ti.name or ti.name.endswith('/.git') else ti)
        print('tarball', os.path.relpath(tgz, ROOT))
    print('packaged', os.path.relpath(out, ROOT), 'versions', [e['version'] for e in entries], 'latest', latest)


if __name__ == '__main__':
    main()
