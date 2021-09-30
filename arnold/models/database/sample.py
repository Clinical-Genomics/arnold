from typing import Optional
from pydantic import Field
from datetime import datetime
from beanie import Document


class Sample(Document):
    """LIMS Sample Collection"""

    id: Optional[str] = Field(alias="_id")
    sample_id: str
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
