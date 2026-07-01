from playwright.sync_api import sync_playwright
import json
import time


def run(url):
    traffic = []
    def on_request(request):
        traffic.append({
            "type": "request",
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "post_data": request.post_data,
            "resource_type": request.resource_type,
            "timestamp": time.time()
        })
    def on_request(request):
        traffic.append({
        "type": "request",
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
        "post_data": request.post_data,
        "resource_type:": request.resource_type,
        "timestamp": time.time()                                
        })


        def on_response(response):
            entry = {
                "type": "response",
                "url" : response.url,
                "status": response.status,
                "headers": dict(response.headers),
                "timestamp": time.time()
            }

            try:
                body = response.text()
                entry["body"] = body
            except: 
                entry["body"] = None

            traffic.append(entry)

    with sync_playwright as sp:
        browser = sp.chromium.lanuch()
        context = browser.new_contex()
        page = context.new_page()
        page.on("request",on_request)
        page.on("response")

    page.goto(url,wait_until="networkidle")
    page.wait_for_timeout(5000)
    browser.close()

    with open("network_dump.json","w",encoding="utf-8") as file_dump:
        json.dump(traffic,file_dump,indent=2,ensure_ascii=False)


if __name__ == "__main__":
    run(input("Enter url to test: "))
