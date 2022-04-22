from typing import Optional, Literal, List

from pydantic import BaseModel, Field

from arnold.models.database import Step


class WorkflowResponce(BaseModel):
    id: str = Field(..., alias="_id")
    step_types: list[str]


class UDFFilter(BaseModel):
    udf_name: str
    udf_rule: Literal["$lt", "$lte", "$gt", "$gte", "$eq"]
    udf_value: str
    udf_query_type: str
    udf_type: Literal["process", "artifact"]


class StepFiltersBase(BaseModel):
    sample_id: Optional[str] = None
    well_position: Optional[str] = None
    artifact_name: Optional[str] = None
    container_name: Optional[str] = None
    container_id: Optional[str] = None
    container_type: Optional[Literal["96 well plate", "Tube"]] = None
    index_name: Optional[str] = None
    workflow: Optional[str] = None
    step_type: Optional[str] = None


class Pagination(BaseModel):
    page_size: Optional[int] = 5
    page_num: Optional[int] = 0
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend"
    sort_key: Optional[str] = "sample_id"


class StepFilters(StepFiltersBase):
    udf_filters: Optional[list[UDFFilter]] = []


class UDF(BaseModel):
    udf: str
    type: str
    udf_type: Optional[Literal["artifact", "process"]]


class ArtifactUDF(UDF):
    udf: str
    type: str
    udf_type: str = "artifact"


class ProcessUDF(UDF):
    udf: str
    type: str
    udf_type: str = "process"


class SampleSteps(BaseModel):
    sample_id: str
    steps: List[Step]
