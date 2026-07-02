from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger('uvicorn.access')
logger.disabled = True

def register_middleware(app: FastAPI):
    @app.middleware('http')
    async def custom_logging_middleware(request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url.path} started at {start_time}")
        response = await call_next(request)
        end_time = time.time()
        logger.info(f"Request: {request.method} {request.url.path} completed at {end_time}")
        process_time = end_time - start_time
        logger.info(f"Request: {request.method} {request.url.path} completed in {process_time:.4f} seconds")
        return response

    @app.middleware('http')
    async def authorization_middleware(request: Request, call_next):
        if "Authorization" not in request.headers:
            return JSONResponse(status_code=401, content={"message": "Authorization header missing"})
        return await call_next(request)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    