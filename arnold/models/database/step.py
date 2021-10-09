from typing import Optional, Dict
from pydantic import Field, BaseModel

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
    container_name: Optional[str]
    index_name: Optional[str]
    nr_samples: Optional[int]
    artifact_udfs: Optional[Dict[str]]
    process_udfs: Optional[Dict[str]]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
