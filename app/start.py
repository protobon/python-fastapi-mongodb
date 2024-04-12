from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import time

from app.router.api import api_router
from app.common.constants import EnvConstants as Env


def run(config):
    app = FastAPI(
        title=config.app[Env.APP.name]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/login", StaticFiles(directory="app/auth/login", html=True), name="login")
    app.include_router(api_router)

    @app.middleware("http")
    async def add_process_time_header(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
        return response

    uvicorn.run(app, host=config.app[Env.APP.host], port=config.app[Env.APP.port])
