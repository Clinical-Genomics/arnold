from typing import Optional
from pydantic import Field, BaseModel, validator
from datetime import datetime


class Sample(BaseModel):
    """LIMS Sample Collection"""

    sample_id: str
    id: Optional[str] = Field(..., alias="_id")
    application_tag: Optional[str]
    category: Optional[str]
    received_date: Optional[datetime]
    delivery_date: Optional[datetime]
    sequenced_date: Optional[datetime]
    prepared_date: Optional[datetime]
    sequenced_to_delivered: Optional[int]
    prepped_to_sequenced: Optional[int]
    received_to_prepped: Optional[int]
    received_to_delivered: Optional[int]
    family: Optional[str]
    strain: Optional[str]
    source: Optional[str]
    customer: Optional[str]
    priority: Optional[str]
    initial_qc: Optional[str]
    library_qc: Optional[str]
    prep_method: Optional[str]
    sequencing_qc: Optional[str]

    @validator("id", always=True)
    def set_id(cls, v, values: dict) -> str:
        """sett _id to prep_id"""

        return values.get("sample_id")

    class Config:
        allow_population_by_field_name = True
