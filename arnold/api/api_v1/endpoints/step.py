from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from arnold.adapter import ArnoldAdapter
from arnold.crud import create, update, read
from arnold.models.database.step import Step
import logging

from arnold.models.query_params import StepsQuery
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/workflows")
def get_workflows(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available workflows in the database"""
    return adapter.step_collection.distinct("workflow")


@router.get("/step/step_types")
def get_step_types(
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available workflows in the database"""
    return adapter.step_collection.find({"workflow": {"$eq": workflow}}).distinct("step_type")


@router.get("/step/step_type/process_udfs")
def get_step_type_process_udfs(
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a step by step id"""
    return read.find_step_type_process_udfs(
        adapter=adapter, step_type=step_type, workflow=workflow, udf_from="process"
    )


@router.get("/step/step_type/artifact_udfs")
def get_step_type_artifact_udfs(
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a step by step id"""
    return read.find_step_type_process_udfs(
        adapter=adapter, step_type=step_type, workflow=workflow, udf_from="artifact"
    )


@router.get("/step/{step_id}", response_model=Step)
def get_step_by_id(
    step_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a step by step id"""
    step: Step = read.find_step(step_id=step_id, adapter=adapter)
    return step


@router.get("/steps/", response_model=List[Step])
def get_steps(
    steps_query: StepsQuery = Depends(StepsQuery),
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get all steps"""

    steps: List[Step] = read.query_steps(adapter=adapter, **steps_query.dict())

    return steps


@router.post("/step/")
def create_step(step: Step, adapter: ArnoldAdapter = Depends(get_arnold_adapter)) -> JSONResponse:
    if read.find_step(step_id=step.step_id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content="step already in database"
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
def update_step(step: Step, adapter: ArnoldAdapter = Depends(get_arnold_adapter)) -> JSONResponse:

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
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"steps inserted to db")
