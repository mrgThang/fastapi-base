import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.core.security import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.schema import UpsertProductGroupReq, UpsertSolutionReq, GetCategoriesReq, UpsertCategoryReq
from app.services.service import Service

logger = logging.getLogger()
router = APIRouter()


@router.get("")
def get(req: GetCategoriesReq = Depends()) -> Any:
    try:
        return DataResponse().success_response(data=Service().get_categories(req))
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.post("", dependencies=[Depends(login_required)])
def post(req: UpsertCategoryReq) -> Any:
    try:
        Service().upsert_category(req)
        return DataResponse().success_response(data=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))
