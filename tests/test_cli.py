import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from tikguard import cli, recovery, reports, security


def run_cli(inputs, argv=None):
    out = io.StringIO()
    with mock.patch("builtins.input", side_effect=inputs), \
            contextlib.redirect_stdout(out):
        code = cli.main(argv if argv is not None else [])
    return code, out.getvalue()


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        patcher = mock.patch.dict(os.environ, {"TIKGUARD_HOME": self.tmp.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_menu_and_exit(self):
        code, out = run_cli(["0"])
        self.assertEqual(code, 0)
        self.assertIn("Username Scanner", out)

    def test_invalid_selection(self):
        code, out = run_cli(["99", "abc", "0"])
        self.assertEqual(code, 0)
        self.assertIn("Invalid selection", out)

    def test_keyboard_interrupt(self):
        code, out = run_cli(KeyboardInterrupt())
        self.assertEqual(code, 130)

    def test_eof_exits_cleanly(self):
        code, _ = run_cli(EOFError())
        self.assertEqual(code, 130)

    def test_scanner_flow(self):
        code, out = run_cli(["1", "@good_user", "n", "", "", "0"])
        self.assertIn("https://www.tiktok.com/@good_user", out)

    def test_scanner_invalid(self):
        _, out = run_cli(["1", "bad name!", "", "0"])
        self.assertIn("Invalid", out)

    def test_report_flow_is_local_only(self):
        inputs = ["2", "1", "https://www.tiktok.com/@fake_acc",
                  "Pretends to be me using my photos", "screenshot1.png", "",
                  "", "n", "", "0"]
        _, out = run_cli(inputs)
        self.assertIn("NOT submitted", out)

    def test_version_and_diagnostics(self):
        code, out = run_cli([], ["--version"])
        self.assertEqual(code, 0)
        self.assertIn("TikGuard CLI", out)
        with mock.patch("tikguard.cli.online", return_value=False):
            code, out = run_cli([], ["diagnostics"])
        self.assertEqual(code, 0)
        self.assertIn("offline", out)

    def test_links_are_official_https(self):
        for links in (recovery.OFFICIAL_LINKS, reports.OFFICIAL_LINKS,
                      security.OFFICIAL_LINKS):
            for url in links.values():
                self.assertTrue(url.startswith("https://"))
                self.assertIn("tiktok.com", url)

    def test_case_manager_flow(self):
        inputs = ["1", "@abc_def", "n", "my note", "",
                  "5", "1", "2", "1", "3", "1", "4", "1", "0", "", "0"]
        _, out = run_cli(inputs)
        self.assertIn("case #1", out)
        self.assertIn("Exported to", out)
        self.assertIn("Deleted.", out)


if __name__ == "__main__":
    unittest.main()
