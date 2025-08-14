from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

from app.notifications import get_channel

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/stream/{request_id}")
async def stream(request_id: str):
    queue = get_channel(request_id)

    async def event_generator():
        while True:
            msg = await queue.get()
            yield f"data: {msg}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


