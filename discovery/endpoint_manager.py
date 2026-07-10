from .endpoint import Endpoint


class EndpointManager:

    def __init__(self):
        self.endpoints = {}

    def add_request(self, path, method, resource_type, request):

        if path not in self.endpoints:
            self.endpoints[path] = Endpoint(path)

        endpoint = self.endpoints[path]

        endpoint.methods.add(method)
        endpoint.resource_types.add(resource_type)
        endpoint.requests.append(request)
        endpoint.times_seen += 1

    def add_response(self, path, response):

        if path not in self.endpoints:
            self.endpoints[path] = Endpoint(path)

        self.endpoints[path].responses.append(response)

    def get_all(self):
        return self.endpoints.values()