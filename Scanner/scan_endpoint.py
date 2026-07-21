import regex

def scan_endpoint(endpoint,params):
    for params in endpoint.requests:
        print(f"Methods: {endpoint.methods}")

    

def tests_patterns(pattern):
    if pattern == False:
        pattern = True
    elif regex.match([0-9] in pattern):
        return pattern+1,pattern-1
    
    else:
        return pattern

