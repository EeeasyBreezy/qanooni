from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.common.ContentTypes import ContentType
from app.dependencies import get_upload_service
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File as AppFile


router = APIRouter(prefix="/upload", tags=["upload"])

async def map_file(file: UploadFile) -> AppFile:
    return AppFile(
        file_name=file.filename,
        mime_type=file.content_type,
        size_bytes=len(await file.read()),
        content=await file.read()
    )

@router.post("")
async def upload_files(
    files: List[UploadFile] = File(...),
    service: IUploadService = Depends(get_upload_service),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    app_files: List[AppFile] = []
    for f in files:
        if f.content_type not in {ContentType.pdf, ContentType.docx}:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {f.content_type}")
        app_files.append(await map_file(f))

    result = service.upload_files(app_files)
    return {"result": result}


