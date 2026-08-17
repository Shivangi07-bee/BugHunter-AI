from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4


@dataclass
class PlannedRequest:

    id: str = field(default_factory=lambda: str(uuid4()))

    endpoint: str = ""

    method: str = "GET"

    headers: Dict = field(default_factory=dict)

    parameters: Dict = field(default_factory=dict)

    body: Dict = field(default_factory=dict)

    purpose: str = ""

    priority: int = 0


class RequestPlanner:

    """
    Converts attack plans into investigation requests.
    """

    def __init__(self):

        self.requests = []

    # -----------------------------------------

    def add_request(

        self,

        endpoint,

        method,

        purpose,

        priority=50,

        headers=None,

        parameters=None,

        body=None

    ):

        request = PlannedRequest(

            endpoint=endpoint,

            method=method,

            purpose=purpose,

            priority=priority,

            headers=headers or {},

            parameters=parameters or {},

            body=body or {}

        )

        self.requests.append(request)

    # -----------------------------------------

    def next_request(self):

        if not self.requests:

            return None

        self.requests.sort(

            key=lambda r: r.priority,

            reverse=True

        )

        return self.requests.pop(0)

    # -----------------------------------------

    def remaining(self):

        return len(self.requests)