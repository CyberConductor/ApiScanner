from playwright.sync_api import sync_playwright

from browser.collector import NetworkCollector
from .queue import Urlqueue
from .extractor import Extractor


class Crawler:
    def __init__(self, collector=None):
        self.collector = collector or NetworkCollector()
        self.queue = Urlqueue()
        self.extractor = Extractor()

    def crawl(self, start_url):
        self.queue.add_url(start_url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.on("request", self.collector.handle_request)
            page.on("response", self.collector.handle_response)

            while True:
                url = self.queue.get_next_url()
                if not url:
                    break

                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(500)
                links = self.extractor.extract_links(page, url)

                for link in links:
                    self.queue.add_url(link)

            browser.close()

        return self.collector.manager