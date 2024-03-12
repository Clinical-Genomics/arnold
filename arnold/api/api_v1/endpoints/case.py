from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from arnold.crud import create, read
from arnold.adapter.plugin import ArnoldAdapter
from arnold.settings import get_arnold_adapter
from arnold.models.database.case.case import Case

router = APIRouter()
import logging

LOG = logging.getLogger(__name__)


@router.post(
    "/case/",
    response_description="Create a new case document",
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    case: Case = Body(...),
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
) -> JSONResponse:
    """Create a case document in the database."""
    try:
        existing_case = read.case.get_case(case_id=case.id, adapter=adapter)
        if existing_case:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "error": "Case already in database.",
                    "existing_case": existing_case,
                },
            )

        create.create_case(case=case, adapter=adapter)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=f"Case with {case.id} was created.",
        )
    except Exception as error:
        # Log the error for debugging purposes
        LOG.error(f"Error creating case: {error}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Failed to create case. Details: {error}"},
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
