from typing import Optional, Literal, List

from fastapi import Query
from pydantic import BaseModel


class BaseQuery(BaseModel):
    page_size: Optional[int] = 5
    page_num: Optional[int] = 0
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend"
    sort_key: Optional[str] = "sample_id"
    well_position: Optional[str] = None
    artifact_name: Optional[str] = None
    container_name: Optional[str] = None
    container_id: Optional[str] = None
    container_type: Optional[Literal["96 well plate", "Tube"]] = None
    index_name: Optional[str] = None


class StepsQuery(BaseQuery):
    workflow: Optional[str] = None
    step_type: Optional[str] = None
