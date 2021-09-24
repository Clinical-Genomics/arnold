from typing import List, Dict

from fastapi import APIRouter, Depends, Response, status
from pymongo.errors import BulkWriteError
from fastapi.responses import JSONResponse

from arnold.crud.read import find_prep
from arnold.exceptions import InsertError
from arnold.models.database.prep.prep import Prep
import logging

LOG = logging.getLogger(__name__)

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
async def create_prep(response: Response, prep: Prep):
    if Prep.find_one(Prep.id == prep.id):
        return "Prep already in database"
    try:
        await prep.create()
        LOG.info("Prep %s inserted to the database", prep.prep_id)
    except:
        raise InsertError(message="could not insert")
    return prep


@router.post("/preps/")
async def create_preps(preps: List[Prep]) -> JSONResponse:
    await Prep.insert_many(preps)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Preps inserted to db")
