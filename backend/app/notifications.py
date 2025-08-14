import asyncio
from typing import Dict, Optional

_loop: Optional[asyncio.AbstractEventLoop] = None
_channels: Dict[str, asyncio.Queue[str]] = {}


def set_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    global _loop
    _loop = loop


def get_channel(request_id: str) -> asyncio.Queue[str]:
    if request_id not in _channels:
        _channels[request_id] = asyncio.Queue(maxsize=10)
    return _channels[request_id]


def publish_done(request_id: str, message: str) -> None:
    queue = get_channel(request_id)
    if _loop is None:
        # Best effort fallback
        try:
            queue.put_nowait(message)
        except asyncio.QueueFull:
            pass
        return
    asyncio.run_coroutine_threadsafe(queue.put(message), _loop)


