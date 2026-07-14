import time
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

        data = {
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "post_data": request.post_data,
            "resource_type": request.resource_type,
            "timestamp": time.time()
        }

        ignore_types ={
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

        if not APIClassifier.is_interesting_request(request.response):
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

