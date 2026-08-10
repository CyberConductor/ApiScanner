from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import requests


def get_request_parameters(request):
    parameters = []

    parsed = urlparse(request["url"])

    for name, values in parse_qs(
        parsed.query,
        keep_blank_values=True
    ).items():
        parameters.append({
            "name": name,
            "location": "query",
            "value": values[0]
        })

    for name, value in request.get("headers", {}).items():
        parameters.append({
            "name": name,
            "location": "header",
            "value": value
        })

    body = request.get("body")

    if isinstance(body, dict):
        for name, value in body.items():
            parameters.append({
                "name": name,
                "location": "body",
                "value": value
            })

    return parameters


def mutate_request(request, parameter, new_value):
    mutated = {
        **request,
        "headers": dict(request.get("headers", {}))
    }

    location = parameter["location"]
    name = parameter["name"]

    if location == "query":
        parsed = urlparse(mutated["url"])

        query = parse_qs(
            parsed.query,
            keep_blank_values=True
        )

        query[name] = [new_value]

        new_query = urlencode(
            query,
            doseq=True
        )

        mutated["url"] = urlunparse(
            parsed._replace(query=new_query)
        )

    elif location == "header":
        mutated["headers"][name] = new_value

    elif location == "body":
        body = dict(mutated.get("body", {}))
        body[name] = new_value
        mutated["body"] = body

    return mutated


def send_request(request, session=None):
    session = session or requests.Session()

    return session.request(
        method=request.get("method", "GET"),
        url=request["url"],
        headers=request.get("headers", {}),
        json=request.get("body"),
        timeout=15
    )


def scan_request(request):
    session = requests.Session()

    base_response = send_request(
        request,
        session
    )

    results = []

    parameters = get_request_parameters(request)

    for parameter in parameters:
        mutated_request = mutate_request(
            request,
            parameter,
            "TEST"
        )

        response = send_request(
            mutated_request,
            session
        )

        results.append({
            "parameter": parameter,
            "status": response.status_code,
            "length": len(response.text)
        })

    return {
        "base_status": base_response.status_code,
        "results": results
    }




    def generate_test_values(value):
    value = str(value)

    if value.isdigit():
        number = int(value)

        return [
            "0",
            "-1",
            str(number - 1),
            str(number + 1),
            "999999"
        ]

    return [
        "",
        "TEST",
        value + "TEST"
    ]