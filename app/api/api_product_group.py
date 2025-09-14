import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.core.security import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.schema import UpsertProductGroupReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("")
def get() -> Any:
    try:
        return DataResponse().success_response(data=Service().get_product_groups())
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.post("", dependencies=[Depends(login_required)])
def post(req: UpsertProductGroupReq) -> Any:
    try:
        Service().upsert_product_groups(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))
