from browser.browser import run


url = input("Enter URL to test: ").strip()


manager = run(url)


print("\nDiscovered endpoints:\n")


for endpoint in manager.get_all():

    print(
        f"{endpoint.methods} {endpoint.path} "
        f"Seen: {endpoint.times_seen}"
    )