import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.core.security import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.schema import UpsertProductGroupReq, UpsertSolutionReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("")
def get() -> Any:
    try:
        return DataResponse().success_response(data=Service().get_solutions())
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.post("", dependencies=[Depends(login_required)])
def post(req: UpsertSolutionReq) -> Any:
    try:
        Service().upsert_solution(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.get("/{id}")
def get(id: int) -> Any:
    try:
        return DataResponse().success_response(data=Service().get_solution_detail(id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))
