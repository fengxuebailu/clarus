"""
Minimal test WebSocket routes
"""

from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/api/testws", tags=["TestWebSocket"])


@router.websocket("/simple")
async def websocket_simple(websocket: WebSocket):
    """Ultra-minimal WebSocket endpoint"""
    await websocket.accept()
    await websocket.send_text("Hello from test!")
    await websocket.close()
