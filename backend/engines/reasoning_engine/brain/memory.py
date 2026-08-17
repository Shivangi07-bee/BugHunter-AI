from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class MemoryRecord:
    """
    One memory item stored inside the AI Brain.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    category: str = ""

    title: str = ""

    data: Dict = field(default_factory=dict)

    confidence: float = 0.0

    timestamp: datetime = field(default_factory=datetime.utcnow)

    tags: List[str] = field(default_factory=list)


class BrainMemory:
    """
    Working memory of BugHunter AI.

    Stores:
        - hypotheses
        - evidence
        - decisions
        - attack paths
        - observations
        - verified findings
    """

    def __init__(self):

        self.memory: Dict[str, MemoryRecord] = {}

    # ---------------------------------------------------------

    def remember(
        self,
        category: str,
        title: str,
        data: Dict,
        confidence: float = 0.5,
        tags: Optional[List[str]] = None
    ):

        record = MemoryRecord(

            category=category,

            title=title,

            data=data,

            confidence=confidence,

            tags=tags or []

        )

        self.memory[record.id] = record

        return record

    # ---------------------------------------------------------

    def recall_by_category(self, category: str):

        return [

            record

            for record in self.memory.values()

            if record.category == category

        ]

    # ---------------------------------------------------------

    def recall_by_tag(self, tag: str):

        return [

            record

            for record in self.memory.values()

            if tag in record.tags

        ]

    # ---------------------------------------------------------

    def search(self, keyword: str):

        keyword = keyword.lower()

        results = []

        for record in self.memory.values():

            if keyword in record.title.lower():

                results.append(record)

                continue

            if keyword in str(record.data).lower():

                results.append(record)

        return results

    # ---------------------------------------------------------

    def update_confidence(self, record_id, confidence):

        if record_id not in self.memory:

            return False

        self.memory[record_id].confidence = confidence

        return True

    # ---------------------------------------------------------

    def delete(self, record_id):

        if record_id in self.memory:

            del self.memory[record_id]

            return True

        return False

    # ---------------------------------------------------------

    def all(self):

        return list(self.memory.values())

    # ---------------------------------------------------------

    def summary(self):

        summary = {}

        for record in self.memory.values():

            summary.setdefault(record.category, 0)

            summary[record.category] += 1

        return summary

    # ---------------------------------------------------------

    def clear(self):

        self.memory.clear()