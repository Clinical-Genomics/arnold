from typing import List, Optional, Literal
from fastapi import APIRouter, Depends
from arnold.adapter import ArnoldAdapter
from arnold.crud import read
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trends/over_time")
def get_trends(
    step_type: str,
    workflow: str,
    udf: str,
    group: str,
    year: int,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """"""
    return read.query_trend(
        adapter=adapter, step_type=step_type, workflow=workflow, udf=udf, group=group, year=year
    )


@router.get("/trends/compare")
def get_trends(
    workflow: str,
    udf_x: str,
    udf_y: str,
    step_type_x: str,
    step_type_y: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """"""

    return read.query_compare(
        adapter=adapter,
        workflow=workflow,
        udf_x=udf_x,
        udf_y=udf_y,
        step_type_x=step_type_x,
        step_type_y=step_type_y,
    )
