from typing import Optional
from pydantic import Field, validator, BaseModel

from pydantic import Extra


class Step(BaseModel):
    """Artifact related fields that are not udfs."""

    id: str = Field(..., alias="_id")
    prep_id: str
    step_type: str
    sample_id: str
    workflow: str
    well_position: Optional[str]
    container_name: Optional[str]
    index_name: Optional[str]
    nr_samples: Optional[int]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
