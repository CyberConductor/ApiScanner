from urllib.parse import urlparse,parse_qs

def create_endpoint(method,url,headers=None,body=None):
    parsed = urlparse(url)

    endpoint = {
        "method": method,
        "url": f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
        "query_params": {
            key: values[0]
            for key, values in parse_qs(parsed.query).items()
        },
        "headers": headers or {},
        "body": body
    }

    return endpoint


def get_parameters(endpoint):
    parameters = []

    for name, value in endpoint.get("query_params", {}).items():
        parameters.append({
            "name": name,
            "location": "query",
            "value": value
        })

    for name, value in endpoint.get("headers", {}).items():
        parameters.append({
            "name": name,
            "location": "header",
            "value": value
        })

    body = endpoint.get("body")

    if isinstance(body, dict):
        for name, value in body.items():
            parameters.append({
                "name": name,
                "location": "body",
                "value": value
            })

    return parameters
