from fastapi import FastAPI
from app.routers import parse_router

app = FastAPI(title="Doc Parser Service", version="0.4.0")
app.include_router(parse_router.router)
