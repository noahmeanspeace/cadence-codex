#!/usr/bin/env python3
"""Read-only SSH probe. Python 3.9+, standard library only."""
import argparse
import json
import re
import subprocess
import sys


# Explicit POSIX shell avoids depending on the account's csh/bash syntax.
REMOTE_COMMAND = "sh -s"
REMOTE_SCRIPT = """printf 'CADENCE_PROBE_V1\\n'
printf 'user\\t'; id -un
printf 'host\\t'; hostname
printf 'cwd\\t'; pwd
for tool in virtuoso spectre ocean; do
    value=$(command -v "$tool" 2>/dev/null) || value=''
    printf 'tool:%s\\t%s\\n' "$tool" "$value"
done
printf 'CADENCE_PROBE_END\\n'
"""


def valid_target(value):
    # Deliberately accept simple SSH aliases / user@host, not arbitrary options.
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.@:-]*', value):
        raise argparse.ArgumentTypeError('Use a simple SSH alias or user@host; no spaces or shell syntax.')
    return value


def build_command(target):
    return ['ssh', '-T', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10',
            '-o', 'StrictHostKeyChecking=yes', '-o', 'UpdateHostKeys=no',
            target, REMOTE_COMMAND]


def parse_output(output):
    lines = output.splitlines()
    try:
        start = lines.index('CADENCE_PROBE_V1')
        end = lines.index('CADENCE_PROBE_END', start + 1)
    except ValueError as exc:
        raise ValueError('Incomplete probe output') from exc
    values = dict(line.split('\t', 1) for line in lines[start + 1:end] if '\t' in line)
    if not all(values.get(key) for key in ('user', 'host', 'cwd')):
        raise ValueError('Missing remote identity fields')
    return {'identity': {key: values[key] for key in ('user', 'host', 'cwd')},
            'tools': {key: values.get('tool:' + key) or None
                      for key in ('virtuoso', 'spectre', 'ocean')}}


def probe(target, timeout=25, runner=None):
    runner = runner or subprocess.run
    try:
        result = runner(build_command(target), input=REMOTE_SCRIPT, text=True,
                        encoding='utf-8', errors='replace', capture_output=True,
                        timeout=timeout, check=False)
    except FileNotFoundError:
        return {'status': 'ssh_unavailable'}, 2
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'timeout_seconds': timeout}, 2
    if result.returncode:
        return {'status': 'ssh_failed', 'returncode': result.returncode,
                'stderr': result.stderr.strip()}, 2
    try:
        data = parse_output(result.stdout)
    except ValueError as exc:
        return {'status': 'invalid_response', 'error': str(exc),
                'stderr': result.stderr.strip()}, 2
    return {'status': 'connected', **data,
            'note': 'Command discovery only; GUI, licenses and simulation are untested.'}, 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=valid_target)
    parser.add_argument('--dry-run', action='store_true', help='Print plan without connecting')
    args = parser.parse_args()
    if args.dry_run:
        data, code = {'status': 'dry_run', 'argv': build_command(args.target),
                      'stdin': REMOTE_SCRIPT}, 0
    else:
        data, code = probe(args.target)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    sys.exit(main())
