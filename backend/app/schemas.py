from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    repository: str


class AnalyzeResponse(BaseModel):
    project: str
    status: str
    findings: int

    # ============================================================
# TARGET CONTEXT
# ============================================================

from typing import List


class TargetContextRequest(BaseModel):
    name: str
    base_url: str
    scope: List[str] = []
    source: str = "repository"


class TargetContextResponse(BaseModel):
    name: str
    base_url: str
    target: str
    scope: List[str]
    source: str
    valid: bool