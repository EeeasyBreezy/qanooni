from typing import List

from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends, Form, Response, status
import uuid

from app.common.ContentTypes import ContentType
from app.dependencies import get_upload_service
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File as AppFile


router = APIRouter(prefix="/upload", tags=["upload"])

async def map_file(file: UploadFile, request_id: str) -> AppFile:
    content_bytes = await file.read()
    return AppFile(
        file_name=file.filename,
        mime_type=file.content_type,
        size_bytes=len(content_bytes),
        content=content_bytes,
        request_id=request_id
    )

@router.post("")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    request_id: str = Form(...),
    service: IUploadService = Depends(get_upload_service),
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.content_type not in {ContentType.pdf, ContentType.docx}:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    app_file: AppFile = await map_file(file, request_id)
    service.upload_files([app_file])
    
    return Response(status_code=status.HTTP_202_ACCEPTED)


