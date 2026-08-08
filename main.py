from crawler.crawler import Crawler
from Scanner.scan_endpoint import scan_captured_requests, print_scan_report


def get_endpoints(url):
    crawler = Crawler()
    return crawler.crawl(url)


def get_url():
    if __name__ == "__main__":
        url = input("Enter URL to test: ").strip()
        return url


def collect_captured_requests(manager):
    captured_requests = []
    for endpoint in manager.get_all():
        for request in endpoint.requests:
            if request:
                captured_requests.append(request)
    return captured_requests


def run():
    url = get_url()
    manager = get_endpoints(url)

    print("\nDiscovered endpoints:\n")

    for endpoint in manager.get_all():
        print(
            f"{endpoint.methods} {endpoint.path} "
            f"Seen: {endpoint.times_seen}"
        )

    captured_requests = collect_captured_requests(manager)
    print(f"\nCaptured {len(captured_requests)} API requests.")

    scan_choice = input("Run tampering scan on captured API requests? [y/N]: ").strip().lower()
    if scan_choice == "y":
        print("\nStarting tampering scan...\n")
        results = scan_captured_requests(captured_requests)
        for report in results:
            print_scan_report(report)
            print()
    else:
        print("Skipping scan.")
       