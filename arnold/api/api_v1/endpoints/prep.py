from typing import List

from fastapi import APIRouter, Depends

from arnold.crud.read import find_prep
from arnold.models.database.prep.prep import Prep


router = APIRouter()


@router.get("/prep/{prep_id}", response_model=Prep)
async def get_prep_by_id(prep: Prep = Depends(find_prep)):
    """fetch a prep by prep id"""
    return prep


@router.get("/preps/", response_model=List[Prep])
async def get_preps():
    """Get all preps"""
    return await Prep.find_all().to_list()


@router.post("/prep/", response_model=Prep)
async def create_prep(prep: Prep):
    await prep.create()
    return prep
