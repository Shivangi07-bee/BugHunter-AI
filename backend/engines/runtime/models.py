from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4


# ---------------------------------------------------------
# Runtime Step Result
# ---------------------------------------------------------

@dataclass
class RuntimeStep:

    id: str = field(default_factory=lambda: str(uuid4()))

    step_number: int = 0

    action: str = ""

    request: Dict = field(default_factory=dict)

    response_status: int = 0

    response_headers: Dict = field(default_factory=dict)

    response_body: str = ""

    observations: List[str] = field(default_factory=list)

    success: bool = False


# ---------------------------------------------------------
# Runtime Investigation Result
# ---------------------------------------------------------

@dataclass
class RuntimeResult:

    id: str = field(default_factory=lambda: str(uuid4()))

    strategy: str = ""

    objective: str = ""

    priority: int = 0

    steps: List[RuntimeStep] = field(default_factory=list)