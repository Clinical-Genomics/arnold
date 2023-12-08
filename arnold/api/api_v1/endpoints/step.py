from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as

from arnold.adapter import ArnoldAdapter
from arnold.constants import QUERY_RULES
from arnold.crud import create, update
from arnold.crud.read.step import (
    aggregate_step,
    find_step_type_artifact_udfs,
    find_step_type_process_udfs,
    find_step,
    query_steps,
)
from arnold.models.database.step import Step
import logging

from arnold.models.api_models import (
    WorkflowResponce,
    StepFilters,
    StepFiltersBase,
    Pagination,
)
from arnold.settings import get_arnold_adapter
import arnold.crud.read.step

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/step/query_rules")
def get_query_rules():
    """Get possible filtering rules."""

    return QUERY_RULES


@router.get("/step/workflows", response_model=list[WorkflowResponce])
def get_workflows(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
) -> list[WorkflowResponce]:
    """Get available workflows and step types from the step collection."""
    pipe = [{"$group": {"_id": "$workflow", "step_types": {"$addToSet": "$step_type"}}}]
    workflows: list[dict] = aggregate_step(adapter=adapter, pipe=pipe)
    return [WorkflowResponce.model_validate(workflow) for workflow in workflows]


@router.get("/step/step_type/udfs")
def get_step_type_udfs(
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available artifact udfs for a step type"""

    artifact_udfs = find_step_type_artifact_udfs(
        adapter=adapter, step_type=step_type, workflow=workflow
    )
    process_udfs = find_step_type_process_udfs(
        adapter=adapter, step_type=step_type, workflow=workflow
    )
    return artifact_udfs + process_udfs


@router.get("/step/{step_id}", response_model=Step)
def get_step_by_id(
    step_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a step by step id"""

    step: Step = find_step(step_id=step_id, adapter=adapter)
    return step


@router.post("/get_steps/", response_model=List[Step])
def get_steps(
    step_filters: StepFilters,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get steps based on filters"""

    steps: List[Step] = query_steps(
        step_filters=StepFiltersBase.model_validate(step_filters.model_dump()),
        pagination=Pagination.model_validate(step_filters.model_dump()),
        udf_filters=step_filters.udf_filters,
        adapter=adapter,
    )
    return steps


@router.post("/step/")
def create_step(
    step: Step, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    if arnold.crud.read.step.find_step(step_id=step.step_id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"Step: {step.step_id} is already in database",
        )
    try:
        create.create_step(adapter=adapter, step=step)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"step {step.step_id} inserted to db"
    )


@router.post("/steps/")
def create_steps(
    steps: List[Step], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        create.create_steps(adapter=adapter, steps=steps)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="steps inserted to db")


@router.put("/step/")
def update_step(
    step: Step, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        update.update_step(adapter=adapter, step=step)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"step {step.step_id} inserted to db"
    )


@router.put("/steps/")
def update_steps(
    steps: List[Step], adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    try:
        update.update_steps(adapter=adapter, steps=steps)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="steps inserted to db")
