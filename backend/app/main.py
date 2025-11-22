from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import requests as requests_router

app = FastAPI(title="REM KYC Onboarding - MongoDB")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(requests_router.router)
