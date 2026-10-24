import json
import tempfile
import unittest
from pathlib import Path

from tikguard import cases, reports
from tikguard.storage import connect


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "t.db")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_fresh_db_and_crud(self):
        self.assertEqual(cases.list_cases(self.conn), [])
        cid = cases.create_case("note", "profile-note",
                                "https://www.tiktok.com/@abc", "hello",
                                conn=self.conn)
        self.assertEqual(len(cases.list_cases(self.conn)), 1)
        self.assertEqual(cases.get_case(cid, self.conn)["description"], "hello")
        self.assertTrue(cases.delete_case(cid, self.conn))
        self.assertIsNone(cases.get_case(cid, self.conn))

    def test_sql_injection_is_inert(self):
        evil = "x'); DROP TABLE cases;--"
        cid = cases.create_case("note", "profile-note", evil, evil, evil, evil,
                                conn=self.conn)
        self.assertEqual(cases.get_case(cid, self.conn)["description"], evil)
        self.assertEqual(len(cases.list_cases(self.conn)), 1)
        with self.assertRaises(ValueError):
            cases.get_case("1 OR 1=1", self.conn)

    def test_export(self):
        cid = cases.create_case("note", "profile-note", "u", "desc",
                                conn=self.conn)
        out = cases.export_case(cid, Path(self.tmp.name) / "ex", self.conn)
        self.assertEqual(json.loads(out.read_text())["id"], cid)
        with self.assertRaises(KeyError):
            cases.export_case(999, Path(self.tmp.name), self.conn)

    def test_validation(self):
        with self.assertRaises(ValueError):
            cases.create_case("bogus", "scam", "u", "d", conn=self.conn)
        with self.assertRaises(ValueError):
            cases.create_case("note", "scam", "u", "   ", conn=self.conn)

    def test_report_rules(self):
        with self.assertRaises(ValueError):
            reports.prepare_report("1", "http://bad", "long enough text here")
        with self.assertRaises(ValueError):
            reports.prepare_report("1", "https://www.tiktok.com/@abc", "short")
        with self.assertRaises(ValueError):
            reports.prepare_report("9", "https://www.tiktok.com/@abc",
                                   "long enough text here")

    def test_delete_all_and_submitted_flag(self):
        a = cases.create_case("note", "profile-note", "u", "d", conn=self.conn)
        cases.create_case("note", "profile-note", "u", "d", conn=self.conn)
        self.assertEqual(cases.get_case(a, self.conn)["submitted"], 0)
        cases.mark_submitted(a, conn=self.conn)
        self.assertEqual(cases.get_case(a, self.conn)["submitted"], 1)
        self.assertEqual(cases.delete_all(self.conn), 2)


if __name__ == "__main__":
    unittest.main()
