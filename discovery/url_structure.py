import re


class Normalizer:

    @staticmethod
    def normalize(path):

        path = re.sub(r"/\d+", "/{id}", path)

        path = re.sub(
            r"/[0-9a-fA-F-]{36}",
            "/{uuid}",
            path
        )

        return path