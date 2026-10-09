#!/usr/bin/env python3
"""
pipeline.py - Run every build and validation tool of this repository for one API version, in the
order the artefacts depend on each other, and stop at the first stage that fails.

    sources   python3 tools/validate_api_docs.py --strict --version <V>      the authored documents are sound
    oas       make -C tools/zenesis-oas check VERSION=<V>                    vendor keys have rules, tests, lossless
              make -C tools/zenesis-oas to-analytics VERSION=<V>             <V>/zenesis-oas -> <V>/oas (domain files)
              make -C tools/zenesis-oas compare VERSION=<V>                  the two sides agree
    okf       python3 tools/okf/build_okf.py --version <V>                   <V>/okf regenerated
              python3 tools/okf/validate_okf.py <V>/okf                      OKF v0.2 conformance, every link resolves
    postman   python3 tools/postman/build_postman.py --version <V>           <V>/postman regenerated
    status    git status --short <V>                                         what changed, for review

Usage:
    python3 tools/api-agent/pipeline.py                      # latest version, every stage
    python3 tools/api-agent/pipeline.py --version v2.0
    python3 tools/api-agent/pipeline.py --only okf postman    # a subset of stages
    python3 tools/api-agent/pipeline.py --from okf            # this stage and the ones after it
    python3 tools/api-agent/pipeline.py --check               # validate and compare only; write nothing

Exit code 0 when every stage passed, 1 at the first failure (that stage's output is printed in full),
2 on usage errors. Standard library only; needs `make` for the oas stage.
"""
import argparse, json, os, subprocess, sys, time

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL_DIR))
STAGES = ['sources', 'oas', 'okf', 'postman', 'status']


def latest_version():
    with open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8') as f:
        return json.load(f)['latest']


def run(label, cmd, env=None, check=True, quiet_ok=True):
    t = time.time()
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    out = (r.stdout + r.stderr).rstrip()
    ok = r.returncode == 0
    mark = 'ok  ' if ok else 'FAIL'
    tail = out.strip().splitlines()[-1] if out.strip() else ''
    print(f'{mark}  {label:52} {time.time() - t:5.1f}s  {tail if (ok and quiet_ok) else ""}'.rstrip())
    if not ok:
        print()
        print('      $ ' + ' '.join(cmd))
        print('      ' + out.replace('\n', '\n      '))
        print()
        if check:
            sys.exit(1)
    return ok, out


def stage_sources(v, a):
    run('sources: validate_api_docs --strict', [sys.executable, 'tools/validate_api_docs.py', '--strict', '--version', v])


def stage_oas(v, a):
    mk = ['make', '--no-print-directory', '-C', 'tools/zenesis-oas', f'VERSION={v}']
    run('oas: make check (inventory, tests, verify)', mk + ['check'])
    if not a.check:
        run('oas: make to-analytics', mk + ['to-analytics'])
    run('oas: make compare (zenesis-oas vs oas)', mk + ['compare'])


def stage_okf(v, a):
    env = dict(os.environ)
    if a.bundle_version:
        env['OKF_BUNDLE_VERSION'] = a.bundle_version
    if not a.check:
        ok, out = run('okf: build_okf', [sys.executable, 'tools/okf/build_okf.py', '--version', v], env=env)
        warns = [l for l in out.splitlines() if l.startswith('WARN') or l.startswith('unresolved links')]
        if warns:
            print('      the builder reported:')
            for l in out.splitlines():
                if l.startswith(('WARN', 'unresolved', '  ', '       ')):
                    print('      ' + l)
            print('      fix the sources (see tools/okf/agent-guide/05-builder-internals.md) and rebuild')
            sys.exit(1)
    run('okf: validate_okf', [sys.executable, 'tools/okf/validate_okf.py', f'{v}/okf'])


def stage_postman(v, a):
    cmd = [sys.executable, 'tools/postman/build_postman.py', '--version', v]
    run('postman: build_postman' + (' --check' if a.check else ''), cmd + (['--check'] if a.check else []))


def stage_status(v, a):
    ok, out = run('status: git status --short', ['git', 'status', '--short', '--', v, 'tools'], check=False, quiet_ok=False)
    lines = [l for l in out.splitlines() if l.strip()]
    if lines:
        gen = [l for l in lines if f' {v}/okf/' in l or f' {v}/oas/' in l or f' {v}/postman/' in l]
        src = [l for l in lines if l not in gen]
        print(f'      {len(src)} source/tool file(s) changed, {len(gen)} generated file(s) changed')
        for l in src[:40]:
            print('      ' + l)
        if len(src) > 40:
            print(f'      ... {len(src) - 40} more')
        print('      review with: git diff --stat -- ' + v)
    else:
        print('      working tree clean')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', help='API version directory (default: `latest` in manifest.json)')
    ap.add_argument('--only', nargs='+', choices=STAGES, help='run only these stages')
    ap.add_argument('--from', dest='from_stage', choices=STAGES, help='run this stage and every later one')
    ap.add_argument('--check', action='store_true', help='validate and compare only; regenerate nothing')
    ap.add_argument('--bundle-version', help='OKF bundle content version to stamp (OKF_BUNDLE_VERSION)')
    a = ap.parse_args()
    v = a.version or os.environ.get('API_VERSION') or latest_version()
    if not os.path.isdir(os.path.join(ROOT, v)):
        sys.exit(f'{v}/ does not exist; versions are the vN.N/ directories listed in manifest.json')
    stages = list(STAGES)
    if a.only:
        stages = [s for s in STAGES if s in a.only]
    elif a.from_stage:
        stages = STAGES[STAGES.index(a.from_stage):]
    print(f'analytics-api pipeline  version={v}  stages={",".join(stages)}  mode={"check" if a.check else "build"}')
    print()
    for s in stages:
        globals()['stage_' + s](v, a)
    print()
    print('pipeline passed' if not a.check else 'pipeline check passed')


if __name__ == '__main__':
    main()
