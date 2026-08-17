from dataclasses import dataclass


@dataclass
class InvestigationTask:

    priority: int

    title: str

    reason: str

    status: str = "Pending"