from typing import List

from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends, Form

from app.common.ContentTypes import ContentType
from app.dependencies import get_upload_service
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File as AppFile


router = APIRouter(prefix="/upload", tags=["upload"])

async def map_file(file: UploadFile) -> AppFile:
    content_bytes = await file.read()
    return AppFile(
        file_name=file.filename,
        mime_type=file.content_type,
        size_bytes=len(content_bytes),
        content=content_bytes
    )

@router.post("")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    request_id: str | None = Form(default=None),
    service: IUploadService = Depends(get_upload_service),
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.content_type not in {ContentType.pdf, ContentType.docx}:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    app_file: AppFile = await map_file(file)
    result = service.upload_files([app_file])
    # Single file → single request id
    rid = request_id if request_id else str(result[0])
    return {"request_id": rid}


