class Urlqueue:
    def __init__(self):
        self.queue = []
        self.visted = set()

    def add_url(self, url):
        if not url:
            return

        normalized = url.strip()
        if normalized in self.visted:
            return

        self.queue.append(normalized)
        self.visted.add(normalized)

    def get_next_url(self):
        if self.queue:
            url = self.queue.pop(0)
            self.visted.add(url)
            return url

        return None

    def get_next(self):
        return self.get_next_url()