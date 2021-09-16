from fastapi import FastAPI

from arnold.api.api_v1.endpoints import sample
from arnold.api.api_v1.endpoints import prep


app = FastAPI()

app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
app.include_router(prep.router, prefix="/api/v1", tags=["prep"])
