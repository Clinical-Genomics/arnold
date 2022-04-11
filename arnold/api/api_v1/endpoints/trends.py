from typing import Optional, Literal
from fastapi import APIRouter, Depends, Query

from arnold.crud.read.plot import (
    trend_nr_samples_per_month,
    trend_turn_around_times,
    trend_step_fields,
    compare_step_fields,
)
from arnold.adapter import ArnoldAdapter
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()

GROUP_FIELDS = Literal[
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


@router.get("/trends/dynamic_udfs_over_time")
def get_dynamic_udfs_over_time(
    field: str,
    year: int,
    step_type: str,
    workflow: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    group: Optional[GROUP_FIELDS] = Query(None),
):
    """Endpoint for trending step udf fields over time. Possible to group by sample fields"""
    return trend_step_fields(
        adapter=adapter, step_type=step_type, workflow=workflow, field=field, group=group, year=year
    )


@router.get("/trends/sample_turnaround_times")
def get_sample_turnaround_times(
    field: Literal[
        # "sequenced_to_delivered",
        "prepped_to_sequenced",
        "received_to_prepped",
        # "received_to_delivered",
    ],
    year: int,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    group: Optional[GROUP_FIELDS] = Query(None),
):
    """Endpoint for trending turnaround_times (sample udfs) over time. Possible to group by sample fields"""
    return trend_turn_around_times(adapter=adapter, field=field, group=group, year=year)


@router.get("/trends/nr_samples")
def get_nr_samples_per_month(
    year: int,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    group: Optional[GROUP_FIELDS] = Query(None),
):
    """Endpoint for trending turnaround_times (sample udfs) over time. Possible to group by sample fields"""
    return trend_nr_samples_per_month(adapter=adapter, group=group, year=year)


@router.get("/trends/compare")
def get_trends(
    workflow: str,
    udf_x: str,
    udf_y: str,
    step_type_x: str,
    step_type_y: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Endpoint for comparing udfs"""

    return compare_step_fields(
        adapter=adapter,
        workflow=workflow,
        udf_x=udf_x,
        udf_y=udf_y,
        step_type_x=step_type_x,
        step_type_y=step_type_y,
    )
