from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from pymongo.errors import BulkWriteError

from arnold.api.api_v1.endpoints import sample
from arnold.api.api_v1.endpoints import prep


app = FastAPI()


@app.exception_handler(BulkWriteError)
async def exception_handler(request: Request, exc: BulkWriteError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=exc.details.get("writeErrors")
    )


@app.get("/")
async def root():
    return {"message": "Welcome to arnold"}


app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
app.include_router(prep.router, prefix="/api/v1", tags=["prep"])
