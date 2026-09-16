"""Offline tests: no SSH connection, Cadence installation or credentials required."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/cadence-ssh/scripts/check_connection.py'
spec = importlib.util.spec_from_file_location('probe', SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ConnectionTests(unittest.TestCase):
    def run_result(self, stdout='', stderr='', code=0):
        def runner(argv, **kwargs):
            self.assertEqual(argv[0], 'ssh')
            self.assertNotIn('shell', kwargs)
            self.assertIn('BatchMode=yes', argv)
            self.assertIn('StrictHostKeyChecking=yes', argv)
            self.assertEqual(kwargs['input'], probe.REMOTE_SCRIPT)
            return subprocess.CompletedProcess(argv, code, stdout, stderr)
        return runner

    def test_connected_with_missing_tools(self):
        output = 'banner\nCADENCE_PROBE_V1\nuser\tedatest\nhost\tlab\ncwd\t/home/edatest\ntool:virtuoso\t/opt/eda/virtuoso\ntool:spectre\t\nCADENCE_PROBE_END\n'
        data, code = probe.probe('cadence', runner=self.run_result(output))
        self.assertEqual(code, 0)
        self.assertEqual(data['tools']['virtuoso'], '/opt/eda/virtuoso')
        self.assertIsNone(data['tools']['spectre'])

    def test_authentication_failure(self):
        data, code = probe.probe('cadence', runner=self.run_result(stderr='Permission denied', code=255))
        self.assertEqual(data['status'], 'ssh_failed')
        self.assertEqual(code, 2)

    def test_partial_response(self):
        data, code = probe.probe('cadence', runner=self.run_result('CADENCE_PROBE_V1\n'))
        self.assertEqual(data['status'], 'invalid_response')
        self.assertEqual(code, 2)

    def test_timeout(self):
        def runner(*args, **kwargs):
            raise subprocess.TimeoutExpired('ssh', 25)
        self.assertEqual(probe.probe('cadence', runner=runner)[0]['status'], 'timeout')

    def test_missing_ssh(self):
        def runner(*args, **kwargs):
            raise FileNotFoundError()
        self.assertEqual(probe.probe('cadence', runner=runner)[0]['status'], 'ssh_unavailable')

    def test_reject_unsafe_targets(self):
        for target in ('-oProxyCommand=anything', 'host;id', 'host name', '$(id)', 'host\nother'):
            with self.subTest(target=target), self.assertRaises(argparse.ArgumentTypeError):
                probe.valid_target(target)

    def test_accept_alias_and_user_host(self):
        for target in ('cadence', 'user@eda.example.org', 'user@192.0.2.10'):
            self.assertEqual(probe.valid_target(target), target)


if __name__ == '__main__':
    unittest.main()
