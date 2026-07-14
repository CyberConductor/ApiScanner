from urllib.parse import urlparse


class APIClassifier:

    API_KEYWORDS = (
        "/api",
        "/graphql",
        "/rest",
        "/v1",
        "/v2",
        "/rpc"
    )

    API_CONTENT_TYPES = (
        "application/json",
        "application/graphql",
        "application/problem+json",
    )

    IGNORED_RESOURCE_TYPES = {
        "image",
        "font",
        "media",
    }

    IGNORED_EXTENSIONS = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".css",
        ".woff",
        ".woff2",
        ".ttf",
        ".map",
    )

    @classmethod
    def is_interesting_request(cls, request):

        parsed = urlparse(request.url)

        path = parsed.path.lower()

        if request.resource_type in cls.IGNORED_RESOURCE_TYPES:
            return False

        if path.endswith(cls.IGNORED_EXTENSIONS):
            return False

        if any(keyword in path for keyword in cls.API_KEYWORDS):
            return True

        if request.resource_type in ("xhr", "fetch"):
            return True

        return False