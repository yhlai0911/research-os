"""Capture actual isolated installs; never target the user's personal skills."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / 'evidence'
OUT.mkdir(exist_ok=True)
records = []

def run(label, args, expected=0):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    records.append({'label': label, 'command': args, 'returncode': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr})
    (OUT / 'install-transcript.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print(label, result.returncode, result.stdout[-200:], flush=True)
    if result.returncode != expected:
        raise SystemExit(f'{label} failed: {result.stderr}')

run('source', ['git', 'rev-parse', 'HEAD'])
for harness in ['codex', 'claude-code']:
    target = f'.scratch/tutorial-demo/{harness}/skills'
    for profile in ['core', 'finance-social-science']:
        options = ['--target', target, '--harness', harness]
        if profile != 'core':
            options += ['--profile', profile]
        for action in ['preflight', 'install', 'verify']:
            script = 'verify_install.py' if action == 'verify' else 'install_skills.py'
            args = ['uv', 'run', 'python', 'scripts/' + script] + options
            if action == 'preflight':
                args.append('--dry-run')
            run(f'{harness}-{profile}-{action}', args)

# Deliberately alter only the disposable copy, prove an install refuses conflicts.
conflict = ROOT / '.scratch/tutorial-demo/codex/skills/research-help/SKILL.md'
original = conflict.read_text()
conflict.write_text(original + '\nDisposable tutorial conflict.\n')
try:
    result = subprocess.run(['uv', 'run', 'python', 'scripts/install_skills.py',
                             '--target', '.scratch/tutorial-demo/codex/skills', '--dry-run'],
                            cwd=ROOT, text=True, capture_output=True)
    assert result.returncode != 0 and 'conflict' in (result.stdout + result.stderr).lower()
    assert conflict.read_text() == original + '\nDisposable tutorial conflict.\n'
    records.append({'label': 'conflict-refused', 'command': result.args,
                    'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
                    'user_change_preserved': True})
finally:
    conflict.write_text(original)
(OUT / 'install-transcript.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
print('Captured real Codex/Claude core/profile installs and conflict refusal.')
