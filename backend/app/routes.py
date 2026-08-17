from fastapi import APIRouter

from .schemas import AnalyzeRequest

from .services import BugHunterService

router = APIRouter()

service = BugHunterService()


@router.post("/analyze")

def analyze(

    request: AnalyzeRequest

):

    return service.analyze(

        request.repository

    )