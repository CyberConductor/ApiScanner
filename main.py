from crawler.crawler import Crawler


def run(url):
    crawler = Crawler()
    return crawler.crawl(url)


if __name__ == "__main__":
    url = input("Enter URL to test: ").strip()

    manager = run(url)

    print("\nDiscovered endpoints:\n")

    for endpoint in manager.get_all():
        print(
            f"{endpoint.methods} {endpoint.path} "
            f"Seen: {endpoint.times_seen}"
        )