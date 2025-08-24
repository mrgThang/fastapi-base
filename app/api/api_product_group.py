import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from app.schemas.sche_base import DataResponse
from app.schemas.schema import UpsertProductGroupReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("", response_model=DataResponse)
def get() -> Any:
    try:
        return DataResponse().success_response(data=Service().get_product_groups())
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))

@router.post("", response_model=DataResponse)
def post(req: UpsertProductGroupReq) -> Any:
    try:
        Service().upsert_product_groups(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))
