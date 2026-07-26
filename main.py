from crawler.crawler import Crawler


def get_endpoints(url):
    crawler = Crawler()
    return crawler.crawl(url)

def get_url():
    if __name__ == "__main__":
        url = input("Enter URL to test: ").strip()
        return url


def run():
    url = get_url()
    manager = get_endpoints(url)

    print("\nDiscovered endpoints:\n")

    for endpoint in manager.get_all():
        print(
            f"{endpoint.methods} {endpoint.path} "
            f"Seen: {endpoint.times_seen}"
            )
       