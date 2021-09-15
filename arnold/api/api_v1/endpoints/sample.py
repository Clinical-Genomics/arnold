from typing import List

from fastapi import APIRouter, Depends

from arnold.crud.read import find_sample
from arnold.models.database import Sample


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
async def create_sample(sample: Sample):
    await sample.create()
    return sample
