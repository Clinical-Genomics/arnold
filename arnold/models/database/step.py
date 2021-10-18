from typing import Optional
from pydantic import Field, BaseModel
from datetime import datetime

from pydantic import Extra


class Step(BaseModel):
    """Artifact related fields that are not udfs."""

    id: str = Field(..., alias="_id")
    step_id: str
    prep_id: str
    step_type: str
    sample_id: str
    workflow: str
    lims_step_name: Optional[str]
    well_position: Optional[str]
    container_type: Optional[str]
    container_name: Optional[str]
    container_id: Optional[str]
    index_name: Optional[str]
    nr_samples_in_pool: Optional[int]
    artifact_name: Optional[str]
    artifact_udfs: Optional[dict]
    process_udfs: Optional[dict]
    date_run: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
