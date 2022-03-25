from typing import List, Optional, Literal

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as

from arnold.adapter import ArnoldAdapter
from arnold.constants import QUERY_RULES
from arnold.crud import create, update, read
from arnold.crud.read import aggregate_step
from arnold.models.database.step import Step
import logging

from arnold.models.responce_models import WorkflowResponce
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/step/query_rules")
def get_query_rules():
    """Get possible filtering rules."""
    return QUERY_RULES


@router.get("/step/workflows", response_model=list[WorkflowResponce])
def get_workflows(adapter: ArnoldAdapter = Depends(get_arnold_adapter)):
    """Get available workflows and step types from the step collection"""
    pipe = [{"$group": {"_id": "$workflow", "step_types": {"$addToSet": "$step_type"}}}]
    workflows: list[dict] = aggregate_step(adapter=adapter, pipe=pipe)
    return parse_obj_as(List[WorkflowResponce], workflows)


@router.get("/step/step_type/process_udfs")
def get_step_type_process_udfs(
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available process udfs for a step type"""
    try:
        step_type_udfs: List[str] = read.find_step_type_udfs(
            adapter=adapter, step_type=step_type, workflow=workflow, udf_from="process"
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"Exception: {e} ",
        )
    return step_type_udfs


@router.get("/step/step_type/artifact_udfs")
def get_step_type_artifact_udfs(
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available artifact udfs for a step type"""
    try:
        step_type_udfs: List[str] = read.find_step_type_udfs(
            adapter=adapter, step_type=step_type, workflow=workflow, udf_from="artifact"
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )
    return step_type_udfs


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
    page_size: Optional[int] = 5,
    page_num: Optional[int] = 0,
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend",
    sort_key: Optional[str] = "sample_id",
    well_position: Optional[str] = None,
    artifact_name: Optional[str] = None,
    container_name: Optional[str] = None,
    container_id: Optional[str] = None,
    container_type: Optional[Literal["96 well plate", "Tube"]] = None,
    index_name: Optional[str] = None,
    workflow: Optional[str] = None,
    step_type: Optional[str] = None,
    artifact_udf: Optional[List[str]] = Query(None),
    artifact_udf_rule: Optional[list[str]] = Query(None),
    artifact_udf_value: Optional[list[str]] = Query(None),
    process_udf: Optional[list[str]] = Query(None),
    process_udf_rule: Optional[list[str]] = Query(None),
    process_udf_value: list[Optional[str]] = Query(None),
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get steps based on filters"""

    steps: List[Step] = read.query_steps(
        adapter=adapter,
        page_size=page_size,
        page_num=page_num,
        sort_direction=sort_direction,
        sort_key=sort_key,
        well_position=well_position,
        artifact_name=artifact_name,
        container_name=container_name,
        container_id=container_id,
        container_type=container_type,
        index_name=index_name,
        workflow=workflow,
        step_type=step_type,
        artifact_udf=artifact_udf,
        artifact_udf_rule=artifact_udf_rule,
        artifact_udf_value=artifact_udf_value,
        process_udf=process_udf,
        process_udf_rule=process_udf_rule,
        process_udf_value=process_udf_value,
    )
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
    return JSONResponse(status_code=status.HTTP_200_OK, content="steps inserted to db")
