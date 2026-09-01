from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
import json
import time
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")


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
    
    excluded_headers = {
        "accept-encoding", "user-agent", "connection",
        "cache-control", "pragma", "te"
    }
    
    for name, value in request.get("headers", {}).items():
        if name.lower() not in excluded_headers:
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


def generate_test_values(value):
    value_str = str(value)
    
    try:
        number = int(value_str)
        return [
            "0",
            "-1",
            str(number - 1),
            str(number + 1),
            "999999",
            str(number + 1000)
        ]
    except (ValueError, TypeError):
        pass
    
    return [
        "",
        "TEST",
        value_str + "TEST",
        "' OR '1'='1",
        "<script>alert(1)</script>"
    ]


def mutate_request(request, parameter, new_value):
    mutated = {
        **request,
        "headers": dict(request.get("headers", {}))
    }
    
    location = parameter["location"]
    name = parameter["name"]
    
    if location == "query":
        parsed = urlparse(mutated["url"])
        query = parse_qs(parsed.query, keep_blank_values=True)
        query[name] = [new_value]
        new_query = urlencode(query, doseq=True)
        mutated["url"] = urlunparse(parsed._replace(query=new_query))
        
    elif location == "header":
        mutated["headers"][name] = new_value
        
    elif location == "body":
        body = dict(mutated.get("body", {}))
        body[name] = new_value
        mutated["body"] = body
    
    return mutated


def send_request(request, session=None, timeout=15):
    session = session or requests.Session()
    
    try:
        response = session.request(
            method=request.get("method", "GET"),
            url=request["url"],
            headers=request.get("headers", {}),
            json=request.get("body"),
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        return response
    except requests.exceptions.RequestException as e:
        return None


def compare_responses(original, mutated, parameter_name):
    if mutated is None:
        return {
            "difference": True,
            "reason": "Request failed or timed out"
        }
    
    differences = []
    
    if original.status_code != mutated.status_code:
        differences.append(
            f"Status code changed: {original.status_code} → {mutated.status_code}"
        )
    
    orig_len = len(original.text)
    mut_len = len(mutated.text)
    if abs(orig_len - mut_len) > 10:
        differences.append(
            f"Response length changed: {orig_len} → {mut_len}"
        )
    
    if mutated.status_code >= 500:
        differences.append("Server error in mutated response")
    
    if parameter_name in mutated.text:
        differences.append("Test value reflected in response")
    
    if original.text != mutated.text:
        orig_words = set(original.text.lower().split())
        mut_words = set(mutated.text.lower().split())
        if orig_words and len(orig_words.symmetric_difference(mut_words)) > len(orig_words) * 0.2:
            differences.append("Response content structure changed")
    
    return {
        "difference": len(differences) > 0,
        "reasons": differences
    }


def scan_request(request):
    session = requests.Session()
    findings = []

    try:
        base_response = send_request(request, session)
        if base_response is None:
            return None
    except Exception:
        return None
    
    parameters = get_request_parameters(request)
    for parameter in parameters:
        test_values = generate_test_values(parameter["value"])
        
        for test_value in test_values:
            try:
                mutated_request = mutate_request(request, parameter, test_value)
                mut_response = send_request(mutated_request, session)
                
                if mut_response is None:
                    continue
                comparison = compare_responses(
                    base_response,
                    mut_response,
                    str(test_value)
                )
                
                if comparison["difference"]:
                    finding = {
                        "method": request.get("method", "GET"),
                        "url": request.get("url", ""),
                        "parameter": parameter["name"],
                        "location": parameter["location"],
                        "original_value": parameter["value"],
                        "test_value": test_value,
                        "original_status": base_response.status_code,
                        "test_status": mut_response.status_code if mut_response else None,
                        "reasons": comparison["reasons"],
                        "timestamp": time.time()
                    }
                    findings.append(finding)
                
            except Exception as e:
                continue
    
    return {
        "method": request.get("method", "GET"),
        "url": request.get("url", ""),
        "parameters_tested": len(parameters),
        "findings": findings
    }


def scan_captured_requests(requests_list):
    results = []
    tested_count = 0
    parameter_count = 0
    
    for request in requests_list:
        try:
            result = scan_request(request)
            if result:
                results.append(result)
                tested_count += 1
                parameter_count += result.get("parameters_tested", 0)
        except Exception as e:
            continue
    
    return {
        "summary": {
            "total_requests": len(requests_list),
            "requests_tested": tested_count,
            "parameters_tested": parameter_count,
            "findings_count": sum(len(r.get("findings", [])) for r in results)
        },
        "results": results
    }


def print_scan_report(result):
    if not result:
        print("No results to report.")
        return
    
    findings = result.get("findings", [])
    
    if not findings:
        print(f"✓ {result.get('method')} {result.get('url')}")
        print(f"  No potential issues found.")
        return
    
    for finding in findings:
        print("=" * 60)
        print("[!] Potential Issue Detected")
        print("=" * 60)
        print(f"Method:        {finding.get('method')}")
        print(f"Endpoint:      {finding.get('url')}")
        print(f"Parameter:     {finding.get('parameter')}")
        print(f"Location:      {finding.get('location')}")
        print()
        print(f"Original value: {finding.get('original_value')}")
        print(f"Test value:     {finding.get('test_value')}")
        print()
        print(f"Original status: {finding.get('original_status')}")
        print(f"Test status:     {finding.get('test_status')}")
        print()
        print("Behavioral differences:")
        for reason in finding.get("reasons", []):
            print(f"  • {reason}")
        print()


def save_scan_results_json(scan_results, filename="scan_results.json"):
    try:
        with open(filename, "w") as f:
            json.dump(scan_results, f, indent=2, default=str)
        print(f"\n✓ Scan results saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False