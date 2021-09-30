from arnold.crud.read import find_sample
from arnold.models.database import Sample
from typing import List
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
import logging

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sample/{sample_id}", response_model=Sample)
async def get_sample_by_id(sample: Sample = Depends(find_sample)):
    """fetch a sample by sample id"""
    return sample


@router.get("/samples/", response_model=List[Sample])
async def get_samples():
    """Get all samples"""
    return await Sample.find_all().to_list()


@router.post("/sample/", response_model=Sample)
async def create_sample(response: Response, sample: Sample) -> JSONResponse:
    if Sample.find_one(Sample.id == sample.id):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content="Sample already in database"
        )
    try:
        await sample.create()
        LOG.info("Sample %s inserted to the database", sample.sample_id)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="Sample inserted to db")


@router.post("/samples/")
async def create_samples(samples: List[Sample]) -> JSONResponse:
    try:
        await Sample.insert_many(samples)
        LOG.info("Samples inserted to the database")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="Samples inserted to db")
