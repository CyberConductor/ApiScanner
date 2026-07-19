import unittest
from unittest.mock import patch

import main


class MainFlowTests(unittest.TestCase):
    def test_run_uses_crawler(self):
        class FakeManager:
            def get_all(self):
                return []

        class FakeCrawler:
            def __init__(self):
                self.crawled_urls = []

            def crawl(self, url):
                self.crawled_urls.append(url)
                return FakeManager()

        with patch("main.Crawler", FakeCrawler):
            manager = main.run("https://example.com")

        self.assertEqual(manager.get_all(), [])


if __name__ == "__main__":
    unittest.main()
