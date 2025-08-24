from typing import Any

from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse, UserRegisterRequest

router = APIRouter()


@router.post('', response_model=DataResponse[UserItemResponse])
def register(register_data: UserRegisterRequest) -> Any:
    try:
        exist_user = None
        if exist_user:
            raise Exception('Email already exists')
        register_user = UserService().register_user(register_data)
        return DataResponse().success_response(data=register_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
