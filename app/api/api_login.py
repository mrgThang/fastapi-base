from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.sche_base import DataResponse
from app.schemas.sche_token import Token

router = APIRouter()

@router.post('', response_model=DataResponse[Token])
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != settings.APP_USERNAME or form_data.password != settings.APP_PASSWORD:
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    return DataResponse().success_response({
        'access_token': create_access_token()
    })
