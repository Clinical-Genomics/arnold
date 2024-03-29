from arnold.adapter import ArnoldAdapter
from arnold.crud import create, update
from arnold.crud.read.sample import get_sample_by_id, get_samples
from arnold.crud.read.step import find_sample_fields
from arnold.models.database import LimsSample
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging
import arnold.crud.read.sample
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sample/fields")
def get_sample_fields(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get sample fields"""
    return find_sample_fields(adapter=adapter)


@router.get("/sample/{sample_id}", response_model=LimsSample)
def get_sample(
    sample_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a sample by sample id"""
    sample: LimsSample = get_sample_by_id(sample_id=sample_id, adapter=adapter)
    return sample


@router.get("/samples/", response_model=List[LimsSample])
def get_samples(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get all samples"""
    samples: List[LimsSample] = get_samples(adapter=adapter)

    return samples


@router.post("/sample/")
def create_sample(
    sample: LimsSample, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    if arnold.crud.read.sample.get_sample_by_id(
        sample_id=sample.sample_id, adapter=adapter
    ):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"Sample: sample.sample_id is already in database",
        )
    try:
        create.create_sample(adapter=adapter, sample=sample)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"Sample: {sample.sample_id} inserted to database",
    )


@router.post("/samples/")
def create_samples(
    samples: List[LimsSample], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        create.create_samples(adapter=adapter, samples=samples)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Samples inserted to db"
    )


@router.put("/sample/")
def update_sample(
    sample: LimsSample, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        update.update_sample(adapter=adapter, sample=sample)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"Sample: {sample.sample_id} inserted to database",
    )


@router.put("/samples/")
def update_samples(
    samples: List[LimsSample], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        update.update_samples(adapter=adapter, samples=samples)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Samples inserted to db"
    )
