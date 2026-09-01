from crawler.crawler import Crawler
from Scanner.scan_endpoint import (
    scan_captured_requests,
    print_scan_report,
    save_scan_results_json
)


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


def print_scan_summary(scan_results):
    summary = scan_results.get("summary", {})
    print("\n" + "=" * 60)
    print("API SECURITY SCANNER - SCAN SUMMARY")
    print("=" * 60)
    print(f"Requests captured:   {summary.get('total_requests', 0)}")
    print(f"Requests scanned:    {summary.get('requests_tested', 0)}")
    print(f"Parameters tested:   {summary.get('parameters_tested', 0)}")
    print(f"Potential findings:  {summary.get('findings_count', 0)}")
    print("=" * 60 + "\n")


def run():
    url = get_url()
    if not url:
        print("No URL provided.")
        return
    
    print(f"\nCrawling: {url}")
    print("This may take a minute. Navigate the application naturally.\n")
    
    manager = get_endpoints(url)

    print("\nDiscovered endpoints:\n")
    for endpoint in manager.get_all():
        print(f"  {endpoint.methods} {endpoint.path} (seen: {endpoint.times_seen}x)")

    captured_requests = collect_captured_requests(manager)
    print(f"\nCaptured {len(captured_requests)} API requests.")

    if not captured_requests:
        print("No requests captured. Try navigating the application more.")
        return

    scan_choice = input("\nRun security scan on captured requests? [y/N]: ").strip().lower()
    if scan_choice == "y":
        print("\nStarting security scan...\n")
        scan_results = scan_captured_requests(captured_requests)
        
        print_scan_summary(scan_results)
        
        for result in scan_results.get("results", []):
            print_scan_report(result)
        
        save_choice = input("Save detailed results to JSON? [y/N]: ").strip().lower()
        if save_choice == "y":
            save_scan_results_json(scan_results)
    else:
        print("Scan skipped.")


if __name__ == "__main__":
    run()
