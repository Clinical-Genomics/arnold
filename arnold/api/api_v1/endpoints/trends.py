from typing import List, Optional, Literal
from fastapi import APIRouter, Depends
from arnold.adapter import ArnoldAdapter
from arnold.crud import read
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trends/")
def get_trends(
    step_type: str,
    workflow: str,
    udf: str,
    group: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get available artifact udfs for a step type"""
    return read.query_trend(
        adapter=adapter, step_type=step_type, workflow=workflow, udf=udf, group=group
    )
