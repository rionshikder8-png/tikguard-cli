import unittest

from tikguard.scanner import (is_tiktok_profile_url, profile_url,
                              validate_username)


class ValidationTests(unittest.TestCase):
    def test_valid(self):
        for name in ("ab", "@user_name", "user.name1", "a" * 24):
            self.assertTrue(validate_username(name)[0], name)

    def test_invalid(self):
        for name in ("", "a", "a" * 25, "bad name", "user.", "x/y", "a;b",
                     "../etc", "名前"):
            self.assertFalse(validate_username(name)[0], name)

    def test_url(self):
        self.assertEqual(profile_url("@john_doe"),
                         "https://www.tiktok.com/@john_doe")
        with self.assertRaises(ValueError):
            profile_url("bad name")

    def test_profile_url_check(self):
        self.assertTrue(is_tiktok_profile_url("https://www.tiktok.com/@abc"))
        self.assertFalse(is_tiktok_profile_url("http://evil.com/@abc"))
        self.assertFalse(is_tiktok_profile_url("https://tiktok.com.evil.com/@abc"))


if __name__ == "__main__":
    unittest.main()
