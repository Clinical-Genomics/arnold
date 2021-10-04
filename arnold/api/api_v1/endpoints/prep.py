from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from arnold.adapter import ArnoldAdapter
from arnold.crud import create, update, read
from arnold.models.database.prep.prep import Prep
import logging

from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/prep/{prep_id}", response_model=Prep)
def get_prep_by_id(
    prep_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a prep by prep id"""
    prep: Prep = read.find_prep(prep_id=prep_id, adapter=adapter)
    return prep


@router.get("/preps/", response_model=List[Prep])
def get_preps(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get all preps"""
    preps: List[Prep] = read.find_all_preps(adapter=adapter)

    return preps


@router.post("/prep/")
def create_prep(prep: Prep, adapter: ArnoldAdapter = Depends(get_arnold_adapter)) -> JSONResponse:
    if read.find_prep(prep_id=prep.prep_id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content="Prep already in database"
        )
    try:
        create.create_prep(adapter=adapter, prep=prep)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Prep {prep.prep_id} inserted to db"
    )


@router.post("/preps/")
def create_preps(
    preps: List[Prep], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        create.create_preps(adapter=adapter, preps=preps)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="Preps inserted to db")


@router.put("/prep/")
def update_prep(prep: Prep, adapter: ArnoldAdapter = Depends(get_arnold_adapter)) -> JSONResponse:

    try:
        update.update_prep(adapter=adapter, prep=prep)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"Prep {prep.prep_id} inserted to db"
    )
