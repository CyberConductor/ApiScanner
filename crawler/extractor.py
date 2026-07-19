from urllib.parse import urljoin

class Extractor:

    def extract_links(self,page,base_url):
        links = page.locator('a').evaluate_all('elements => elements.map(e => e.href)')
        result = []

        for link in links:
            if link.startswith('/'):
                link = urljoin(base_url, link)

            result.append(link)
        return result
    