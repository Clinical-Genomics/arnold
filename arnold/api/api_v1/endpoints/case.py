from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from arnold.crud import create, read
from arnold.adapter.plugin import ArnoldAdapter
from arnold.settings import get_arnold_adapter
from arnold.models.database.case import Case

router = APIRouter()


@router.post(
    "/case/",
    response_description="Create a new case document",
    status_code=status.HTTP_201_CREATED,
    response_model=Case,
)
def create_case(
    case: Case = Body(...),
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
) -> JSONResponse:
    """Create a case document in the database."""
    if read.case.get_case(case_id=case.id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content="Case already in database.",
        )
    try:
        create.create_case(case=case, adapter=adapter)
    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content=f"Error: {error}"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=f"Case with {case.id} was created."
    )


@router.get(
    "/case/{case_id}",
    response_description="Get a case document.",
    status_code=status.HTTP_200_OK,
    response_model=Case,
)
def get_case(
    case_id: str, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> Case | JSONResponse:
    """Retrieve a case document from the database."""
    try:
        case: Case = read.case.get_case(case_id=case_id, adapter=adapter)
        return case
    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"Could not find entry with {case_id} in database. {error}",
        )
