from playwright.sync_api import sync_playwright

from browser.collector import NetworkCollector



def run(url):

    collector = NetworkCollector()


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context()

        page = context.new_page()


        page.on(
            "request",
            collector.handle_request
        )

        page.on(
            "response",
            collector.handle_response
        )


        page.goto(
            url,
            wait_until="networkidle"
        )


        page.wait_for_timeout(5000)


        browser.close()


    return collector.manager