from arnold.adapter import ArnoldAdapter
from arnold.crud import create, update, read
from arnold.crud.read import find_sample
from arnold.models.database import Sample
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging

from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sample/{sample_id}", response_model=Sample)
def get_sample(
    sample_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a sample by sample id"""
    sample: Sample = read.find_sample(sample_id=sample_id, adapter=adapter)
    return sample


@router.get("/samples/", response_model=List[Sample])
def get_samples(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get all samples"""
    samples: List[Sample] = read.find_all_samples(adapter=adapter)

    return samples


@router.post("/sample/")
def create_sample(
    sample: Sample, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    if find_sample(sample_id=sample.sample_id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content="Sample already in database"
        )
    try:
        create.create_sample(adapter=adapter, sample=sample)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Sample {sample.sample_id} inserted to db"
    )


@router.post("/samples/")
def create_samples(
    samples: List[Sample], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        create.create_samples(adapter=adapter, samples=samples)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="Samples inserted to db")


@router.put("/sample/")
def update_sample(
    sample: Sample, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:

    try:
        update.update_sample(adapter=adapter, sample=sample)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Sample {sample.sample_id} inserted to db"
    )


@router.put("/samples/")
def update_samples(
    samples: List[Sample], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:

    try:
        update.update_samples(adapter=adapter, samples=samples)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"Samples inserted to db")
