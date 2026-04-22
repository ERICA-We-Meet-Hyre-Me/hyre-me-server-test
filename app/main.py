from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.test import router as test_router
from app.api.routes.menu import router as menu_router

app = FastAPI(title="hyre-me test api")

# Test server: allow all origins/methods/headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FastAPI()
api.include_router(test_router)
api.include_router(menu_router)
app.mount("/api", api)
