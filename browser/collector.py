import time
import json
from urllib import request, response
from urllib.parse import urlparse
from discovery.api_classifier import APIClassifier
from discovery.endpoint_manager import EndpointManager
from discovery.url_structure import Normalizer


class NetworkCollector:

    def __init__(self):
        self.manager = EndpointManager()


    def handle_request(self, request):

        if not APIClassifier.is_interesting_request(request):
            return

        parsed = urlparse(request.url)
        path = Normalizer.normalize(parsed.path)

        body = None
        if request.post_data:
            try:
                if isinstance(request.post_data, str):
                    body = json.loads(request.post_data)
                elif isinstance(request.post_data, bytes):
                    body = json.loads(request.post_data.decode('utf-8'))
                else:
                    body = request.post_data
            except (json.JSONDecodeError, UnicodeDecodeError):
                body = request.post_data

        data = {
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "body": body,
            "resource_type": request.resource_type,
            "timestamp": time.time()
        }

        ignore_types = {
            "image",
            "stylesheet",
            "font",
            "media"
        }

        if request.resource_type in ignore_types:
            return

        self.manager.add_request(
            path,
            request.method,
            request.resource_type,
            data
        )


    def handle_response(self, response):

        if not APIClassifier.is_interesting_request(response):
            return
        
        parsed = urlparse(response.url)
        path = Normalizer.normalize(parsed.path)

        data = {
            "url": response.url,
            "status": response.status,
            "headers": dict(response.headers),
            "timestamp": time.time()
        }

        try:
            data["body"] = response.text()
        except Exception:
            data["body"] = None

        self.manager.add_response(
            path,
            data
        )

