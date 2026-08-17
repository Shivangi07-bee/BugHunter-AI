from fastapi import APIRouter, HTTPException

from app.schemas import (
    TargetContextRequest,
    TargetContextResponse,
)

from investigation.target_context import TargetContext


router = APIRouter(
    prefix="/target",
    tags=["target"],
)


@router.post(
    "/context",
    response_model=TargetContextResponse,
)
def create_target_context(
    request: TargetContextRequest,
):
    target = TargetContext(
        name=request.name,
        base_url=request.base_url,
        scope=request.scope,
        source=request.source,
    )

    if not target.is_valid():
        raise HTTPException(
            status_code=400,
            detail="Invalid target URL",
        )

    return target.to_dict()