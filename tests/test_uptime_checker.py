import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from uptime_checker import check_website, normalize_url, read_sites


class UptimeCheckerTests(unittest.TestCase):
    def test_adds_https_scheme(self):
        self.assertEqual(normalize_url("example.com"), "https://example.com")

    def test_successful_website_is_up(self):
        response = MagicMock()
        response.getcode.return_value = 200
        response.__enter__.return_value = response
        with patch("uptime_checker.urlopen", return_value=response):
            result = check_website("https://example.com")
        self.assertTrue(result.is_up)
        self.assertEqual(result.status, 200)

    def test_network_error_is_down(self):
        with patch("uptime_checker.urlopen", side_effect=URLError("offline")):
            result = check_website("https://example.com")
        self.assertFalse(result.is_up)
        self.assertIsNone(result.status)

    def test_reads_sites_and_ignores_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sites.txt"
            path.write_text("# comment\nexample.com\n\nhttps://github.com\n", encoding="utf-8")
            self.assertEqual(read_sites(str(path)), ["example.com", "https://github.com"])


if __name__ == "__main__":
    unittest.main()
