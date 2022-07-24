from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import tender_committee
from app.auth import authentication

app = FastAPI(title="PROCUREMENT API", docs_url="/docs", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication.router)
app.include_router(tender_committee.router)
