from urllib.parse import urlparse,parse_qs

def parse_endpoint(url):
    parsed = urlparse(url)
    parameters = parse_qs(parsed.query)

    return {
        "url": f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
        "params": parameters
    }