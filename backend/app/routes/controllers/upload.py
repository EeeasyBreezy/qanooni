from typing import List

from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends, Form, Response, status
import uuid

from app.dependencies import get_upload_service
from app.dependencies import get_file_validation_service
from app.services.interfaces.IUploadService import IUploadService
from app.services.interfaces.IFileValidationService import IFileValidationService
from app.services.model.File import File as AppFile


router = APIRouter(prefix="/upload", tags=["upload"])

async def map_file(file: UploadFile, request_id: str, normalized_mime: str, content_bytes: bytes) -> AppFile:
    return AppFile(
        file_name=file.filename,
        mime_type=normalized_mime,
        size_bytes=len(content_bytes),
        content=content_bytes,
        request_id=request_id
    )

@router.post("")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    request_id: str = Form(...),
    service: IUploadService = Depends(get_upload_service),
    validator: IFileValidationService = Depends(get_file_validation_service),
):
    content_bytes = await file.read()
    try:
        normalized_mime = validator.validate_and_get_mime(file.filename, content_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    app_file: AppFile = await map_file(file, request_id, normalized_mime, content_bytes)
    service.upload_files([app_file])
    
    return Response(status_code=status.HTTP_202_ACCEPTED)


