import logging
from app.core.logging import setup_logging

setup_logging()
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.core.logging import setup_logging

logger=logging.getLogger(__name__)
app=FastAPI()


@app.middleware("http")
async def log_requests(request,call_next):
    logger.info(
        "Request:%s %s",
        request.method,
        request.url.path
    )
    response=await call_next(request)
    return response



logger.info("InterviewIQ API started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
         "http://192.168.43.242:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return{
        "message":"InterviewIq Backend Running"
    }
@app.get("/health")
def health():
    return {
        "status":"healthy"
    }

app.include_router(auth_router)