from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from pymongo.errors import BulkWriteError

from arnold.api.api_v1.endpoints import sample
from arnold.api.api_v1.endpoints import step
from arnold.api.api_v1.endpoints import trends
from arnold.api.api_v1.endpoints import flow_cell
from arnold.api.api_v1.endpoints import plots
from arnold.api.api_v1.endpoints import case
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BulkWriteError)
async def exception_handler(request: Request, exc: BulkWriteError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=exc.details.get("writeErrors")
    )


@app.get("/")
async def root():
    return {"message": "Welcome to arnold"}


app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
app.include_router(step.router, prefix="/api/v1", tags=["prep"])
app.include_router(trends.router, prefix="/api/v1", tags=["trends"])
app.include_router(flow_cell.router, prefix="/api/v1", tags=["flow_cell"])
app.include_router(plots.router, prefix="/api/v1", tags=["plots"])
app.include_router(case.router, prefix="/api/v1", tags=["case"])
