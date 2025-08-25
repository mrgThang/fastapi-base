import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.sche_base import DataResponse
from app.schemas.schema import GetProductsReq, UpsertProductReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("", response_model=DataResponse)
def get(req: GetProductsReq = Depends()) -> Any:
    try:
        return DataResponse().success_response(data=Service().get_products(req))
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))

@router.post("", response_model=DataResponse)
def post(req: UpsertProductReq) -> Any:
    try:
        Service().upsert_product(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))

@router.get("/{id}", response_model=DataResponse)
def get(id: int) -> Any:
    try:
        return DataResponse().success_response(data=Service().get_product_detail(id))
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))
