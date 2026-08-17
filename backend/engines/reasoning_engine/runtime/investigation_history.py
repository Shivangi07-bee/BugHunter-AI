from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class InvestigationEvent:

    timestamp: datetime

    event: str

    details: Dict


class InvestigationHistory:

    """
    Stores the complete investigation timeline.
    """

    def __init__(self):

        self.timeline: List[InvestigationEvent] = []

    # ---------------------------------------

    def record(

        self,

        event,

        details=None

    ):

        self.timeline.append(

            InvestigationEvent(

                timestamp=datetime.utcnow(),

                event=event,

                details=details or {}

            )

        )

    # ---------------------------------------

    def events(self):

        return self.timeline

    # ---------------------------------------

    def summary(self):

        return [

            {

                "time": e.timestamp,

                "event": e.event

            }

            for e in self.timeline

        ]