from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import time

from app.router.api import api_router


def get_application() -> FastAPI:
    app = FastAPI(
        title="warehouseAPI"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    return app


def run():
    app = get_application()

    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
        return response

    uvicorn.run(app)
