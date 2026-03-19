"""
Clarus Backend - FastAPI Application
Main entry point for the Go Analysis API
"""

import sys
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uvicorn

from .api.routes import router as go_router
from .api.websocket_routes import router as ws_router
from .api.test_routes import router as test_router
from .core.config import settings
from .core.katago_client import get_katago_client, shutdown_katago_client


class WebSocketCORSMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to handle CORS for both HTTP and WebSocket
    FastAPI's CORSMiddleware doesn't properly handle WebSocket connections
    """
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "*")

        # Log WebSocket connections
        if request.url.path.startswith("/api/ws/"):
            print(f"[WebSocket] Request to {request.url.path} from origin: {origin}")

        # Process the request
        response = await call_next(request)

        # Add CORS headers to HTTP responses (not WebSocket)
        if not request.url.path.startswith("/api/ws/"):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"

        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print("[Clarus] Starting up...")
    try:
        # Initialize KataGo client
        print("[Clarus] Initializing KataGo client...")
        katago = await get_katago_client()
        print("[Clarus] KataGo client ready")
    except Exception as e:
        print(f"[Clarus] Warning: KataGo initialization failed: {e}")
        print("[Clarus] Server will use mock data fallback")

    yield  # Application runs

    # Shutdown
    print("[Clarus] Shutting down...")
    await shutdown_katago_client()
    print("[Clarus] KataGo client stopped")


# Create FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title="Clarus - Go Analysis API",
    description="""
    Clarus Dialectical Engine for Go/Weiqi Analysis

    This API provides superhuman AI Go analysis translated into human-understandable explanations
    through a multi-agent debate system with the "Reconstruction Game" validation loop.

    ## Features

    * **Parallel Simulation**: KataGo analyzes multiple moves simultaneously
    * **Contrastive Learning**: Explains differences between moves (Good vs OK/Bad)
    * **Reconstruction Game**: Validates explanations through blind reconstruction
    * **Natural Language**: Converts mathematical data into Go master wisdom

    ## Architecture

    - **Agent A (Grandmaster)**: KataGo engine - provides ground truth
    - **Agent B (Scribe)**: LLM explainer - translates data to language
    - **Agent C (Profiler)**: LLM verifier - blind reconstruction test
    - **Agent D (Arbiter)**: Mathematical judge - validates quality
    - **Agent E (Delta Hunter)**: Difference analyst - extracts key changes
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware for HTTP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Add custom WebSocket CORS middleware
app.add_middleware(WebSocketCORSMiddleware)

# Include routers
app.include_router(go_router)
app.include_router(ws_router)
app.include_router(test_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Clarus Go Analysis API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
        "endpoints": {
            "analyze": "/api/go/analyze",
            "batch_analyze": "/api/go/analyze/batch",
            "websocket": "/api/go/ws/analyze",
            "health": "/api/go/health",
            "concepts": "/api/go/concepts"
        }
    }


@app.get("/health")
async def health():
    """General health check"""
    return {
        "status": "healthy",
        "service": "clarus-backend",
        "version": "1.0.0"
    }


@app.websocket("/api/direct-test")
async def websocket_direct_test(websocket: WebSocket):
    """WebSocket endpoint defined directly in main.py"""
    await websocket.accept()
    await websocket.send_text("Direct test OK")
    await websocket.close()


if __name__ == "__main__":
    # Run with: python -m app.main
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
