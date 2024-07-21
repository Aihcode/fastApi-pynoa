from fastapi import FastAPI
from  fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

"""

    FASTAPI WEB STORE API

"""

class Config:
    def __init__(self) -> None:
        self.app = FastAPI(title="FastApi Pynoa")
        self.web = APIRouter()
        self.api = APIRouter(prefix="/admin/api")
        self.api_public = APIRouter(prefix="/api/frontstore")
        self.auth = APIRouter(prefix="/auth")
        self.add_middleware()

    def add_middleware(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

        return self.app
    

    def add_routes(self) -> None:
        self.app.include_router(self.web)
        return self.app