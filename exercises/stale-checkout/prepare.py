#!/usr/bin/env python3
"""Create a fictional local Git fixture only. By Instinct for Tal Chaim Damri."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def prepare(target):
    target.mkdir(parents=False, exist_ok=False)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_NAME='Fictional Exercise', GIT_AUTHOR_EMAIL='fixture@example.invalid',
               GIT_COMMITTER_NAME='Fictional Exercise', GIT_COMMITTER_EMAIL='fixture@example.invalid',
               GIT_AUTHOR_DATE='2026-01-01T00:00:00+00:00', GIT_COMMITTER_DATE='2026-01-01T00:00:00+00:00')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(target), *args], env=env, stderr=subprocess.STDOUT, text=True).strip()
    git('init', '-b', 'exercise', '--template=')
    git('config', 'core.autocrlf', 'false')
    git('config', 'commit.gpgsign', 'false')
    revisions = []
    for version in ['old', 'current']:
        (target / 'estimate.py').write_bytes((ROOT / 'repo-files' / (version + '.py')).read_bytes())
        git('add', 'estimate.py')
        git('commit', '-m', 'Fictional ' + version + ' checkpoint')
        revisions.append(git('rev-parse', 'HEAD'))
    meta = json.loads((ROOT / 'revisions.json').read_text())
    if revisions != [meta['expected'], meta['actual']]:
        raise RuntimeError('Fixture hashes differ; do not use this checkout.')
    print('FIXTURE_READY: local only; no remote, model or network calls.')

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('one new output directory required')
        prepare(Path(sys.argv[1]))
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print('FIXTURE_REFUSED: ' + type(error).__name__, file=sys.stderr)
        sys.exit(1)
