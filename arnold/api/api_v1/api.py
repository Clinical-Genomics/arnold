from typing import Type
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, Request, status
from pymongo.errors import BulkWriteError

from arnold.api.api_v1.endpoints import sample
from arnold.api.api_v1.endpoints import prep
from arnold.models.database import Sample, Prep
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from arnold.settings import settings

app = FastAPI()


@app.exception_handler(BulkWriteError)
async def exception_handler(request: Request, exc: BulkWriteError) -> JSONResponse:
    print("exceptiom handler")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=exc.details.get("writeErrors")
    )


@app.get("/")
async def root():
    return {"message": "Welcome to arnold"}


@app.on_event("startup")
async def main():
    # Create Motor client
    client = AsyncIOMotorClient(settings.db_uri)

    # Init Beanie
    await init_beanie(client[settings.db_name], document_models=[Sample, Prep])

    app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
    app.include_router(prep.router, prefix="/api/v1", tags=["prep"])
