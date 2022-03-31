from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, Query
from arnold.adapter import ArnoldAdapter
from arnold.crud import read
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trends/step_fields/over_time")
def get_trends(
    field: str,
    year: int,
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    group: Optional[
        Literal[
            "application",
            "sex",
            "initial_qc",
            "library_qc",
            "prep_method",
            "bait_set",
            "capture_kit",
            "customer",
            "organism",
            "priority",
            "source",
        ]
    ] = Query(None),
):
    """"""
    return read.query_trend_step_fields(
        adapter=adapter, step_type=step_type, workflow=workflow, field=field, group=group, year=year
    )


@router.get("/trends/sample_fields/over_time")
def get_sample_field_trends(
    field: str,
    year: int,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    group: Optional[
        Literal[
            "application",
            "sex",
            "initial_qc",
            "library_qc",
            "prep_method",
            "bait_set",
            "capture_kit",
            "customer",
            "organism",
            "priority",
            "source",
        ]
    ] = Query(None),
):
    """"""
    return read.query_trend_sample_fields(adapter=adapter, field=field, group=group, year=year)


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
