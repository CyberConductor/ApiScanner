import time
from urllib.parse import urlparse

from discovery.endpoint_manager import EndpointManager
from discovery.url_structure import Normalizer


class NetworkCollector:

    def __init__(self):
        self.manager = EndpointManager()


    def handle_request(self, request):

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


        self.manager.add_request(
            path,
            request.method,
            request.resource_type,
            data
        )


    def handle_response(self, response):

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