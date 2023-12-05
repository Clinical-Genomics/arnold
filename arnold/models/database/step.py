from typing import Optional
from pydantic import Field, BaseModel
from datetime import datetime

from pydantic import Extra


class Step(BaseModel):
    """Artifact related fields that are not udfs."""

    prep_id: str
    step_type: str
    sample_id: str
    workflow: str
    lims_step_name: Optional[str] = None
    id: str = Field(..., alias="_id")
    step_id: str
    well_position: Optional[str] = None
    artifact_name: Optional[str] = None
    container_name: Optional[str] = None
    container_id: Optional[str] = None
    container_type: Optional[str] = None
    index_name: Optional[str] = None
    nr_samples_in_pool: Optional[int] = None
    date_run: Optional[datetime] = None
    artifact_udfs: Optional[dict] = {}
    process_udfs: Optional[dict] = {}

    class Config:
        populate_by_name = True
        extra = Extra.allow
