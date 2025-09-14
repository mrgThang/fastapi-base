import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query

from app.core.security import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.schema import GetProductsReq, UpsertProductReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("")
def get(childCategoryIds: Optional[list[int]] = Query(default=[]), productGroupId: int = Query(...)) -> Any:
    try:
        req: GetProductsReq = GetProductsReq(
            product_group_id=productGroupId,
            child_category_ids=childCategoryIds
        )
        return DataResponse().success_response(data=Service().get_products(req))
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.post("", dependencies=[Depends(login_required)])
def post(req: UpsertProductReq) -> Any:
    try:
        Service().upsert_product(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.get("/{id}")
def get(id: int) -> Any:
    try:
        return DataResponse().success_response(data=Service().get_product_detail(id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))
