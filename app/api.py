from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn


def get_application() -> FastAPI:
    app = FastAPI(
        title="warehouseAPI"
    )

    origins = [
        "http://localhost:5173",  # React frontend application
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def run():
    app = get_application()
    uvicorn.run(app)
