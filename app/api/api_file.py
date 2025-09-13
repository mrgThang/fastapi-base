import logging
import random
from datetime import datetime
from io import BytesIO
from typing import Any

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, UploadFile
from starlette.responses import StreamingResponse

from app.core.config import settings
from app.schemas.sche_base import DataResponse
from app.schemas.schema import UploadFileResp

logger = logging.getLogger()
router = APIRouter()


@router.get("/download/{filename}")
def download_file(filename: str) -> Any:
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            endpoint_url=settings.MINIO_ENDPOINT if settings.ENVIRONMENT == 'development' else None,
            region_name=settings.AWS_REGION,
        )

        # 1. Lấy content type từ metadata trong S3
        content_type = None
        try:
            head = s3_client.head_object(Bucket=settings.AWS_BUCKET_NAME, Key=filename)
            content_type = head.get("ContentType")
        except Exception:
            content_type = None
        if content_type == None:
            content_type = "application/octet-stream"

        # 2. Download file
        file_stream = BytesIO()
        s3_client.download_fileobj(settings.AWS_BUCKET_NAME, filename, file_stream)
        file_stream.seek(0)

        return StreamingResponse(file_stream, media_type=content_type, headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=logger.error(e))

@router.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            endpoint_url=settings.MINIO_ENDPOINT if settings.ENVIRONMENT == 'development' else None,
            region_name=settings.AWS_REGION,
        )

        # 1. check if bucket exist
        try:
            s3_client.head_bucket(Bucket=settings.AWS_BUCKET_NAME)
        except ClientError:
            location = {'LocationConstraint': settings.AWS_REGION}
            s3_client.create_bucket(Bucket=settings.AWS_BUCKET_NAME, CreateBucketConfiguration=location)

        # 2. handle duplicate filename
        filename: str = file.filename
        file_exist = False
        datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        try:
            s3_client.stat_object(bucket_name=settings.AWS_BUCKET_NAME, object_name=filename)
            file_exist = True
        except Exception:
            file_exist = False
        if file_exist:
            random_prefix = random.randint(1, 1000)
            filename = f"{datetime_prefix}___{random_prefix}___{filename}"
        else:
            filename = f"{datetime_prefix}___{filename}"

        # 3. upload file
        s3_client.upload_fileobj(file.file, settings.AWS_BUCKET_NAME, filename)
        resp = UploadFileResp(filename=filename)

        return DataResponse().success_response(data=resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=logger.error(e))

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