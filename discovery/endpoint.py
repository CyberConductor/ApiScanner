from dataclasses import dataclass, field


@dataclass
class Endpoint:

    path: str
    methods: set = field(default_factory=set)

    requests: list = field(default_factory=list)
    responses: list = field(default_factory=list)

    resource_types: set = field(default_factory=set)

    times_seen: int = 0