import logging
import random
from datetime import datetime
from io import BytesIO
from typing import Any

from minio import Minio
from minio.error import S3Error
from fastapi import APIRouter, HTTPException, UploadFile, Depends
from starlette.responses import StreamingResponse

from app.core.config import settings
from app.core.security import login_required
from app.schemas.sche_base import DataResponse
from app.schemas.schema import UploadFileResp

logger = logging.getLogger()
router = APIRouter()


def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.AWS_ACCESS_KEY,
        secret_key=settings.AWS_SECRET_KEY,
        secure=False if settings.ENVIRONMENT == 'development' else True
    )


@router.get("/download/{filename}")
def download_file(filename: str) -> Any:
    try:
        client = get_minio_client()
        content_type = "application/octet-stream"
        try:
            stat = client.stat_object(settings.AWS_BUCKET_NAME, filename)
            content_type = getattr(stat, "content_type", content_type) or content_type
        except S3Error:
            pass

        obj = client.get_object(settings.AWS_BUCKET_NAME, filename)

        def iter_file():
            try:
                for chunk in obj.stream(32 * 1024):
                    yield chunk
            finally:
                obj.close()
                obj.release_conn()

        return StreamingResponse(iter_file(), media_type=content_type, headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        })
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload", dependencies=[Depends(login_required)])
async def upload_file(file: UploadFile):
    try:
        client = get_minio_client()
        bucket_name = settings.AWS_BUCKET_NAME

        # 1. check if bucket exist
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        # 2. handle duplicate filename
        filename: str = file.filename
        file_exist = False
        datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        try:
            client.stat_object(bucket_name, filename)
            file_exist = True
        except S3Error:
            file_exist = False
        if file_exist:
            random_prefix = random.randint(1, 1000)
            filename = f"{datetime_prefix}___{random_prefix}___{filename}"
        else:
            filename = f"{datetime_prefix}___{filename}"

        # 3. upload file
        file.file.seek(0, 2)
        length = file.file.tell()
        file.file.seek(0)
        content_type = getattr(file, "content_type", None) or from_file_type_to_mime_type(file.filename.split(".")[-1].lower())
        client.put_object(bucket_name, filename, file.file, length, content_type=content_type)
        resp = UploadFileResp(filename=filename)

        return DataResponse().success_response(data=resp)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def from_file_type_to_mime_type(file_type: str) -> str:
    FILE_TYPE_TO_MIME = {
        'rar': 'application/vnd.rar',
        'zip': 'application/zip',
        'png': 'image/png',
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return FILE_TYPE_TO_MIME.get(file_type, 'application/octet-stream')