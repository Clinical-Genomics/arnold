from typing import Optional
from pydantic import Field, BaseModel, validator
from datetime import datetime


class LimsSample(BaseModel):
    """LIMS Sample Collection."""

    sample_id: str
    id: Optional[str] = Field(..., alias="_id")
    ticket: Optional[str] = None
    received_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    sequenced_date: Optional[datetime] = None
    prepared_date: Optional[datetime] = None
    collection_date: Optional[datetime] = None
    category: Optional[str] = None
    sequenced_to_delivered: Optional[int] = None
    prepped_to_sequenced: Optional[int] = None
    received_to_prepped: Optional[int] = None
    received_to_delivered: Optional[int] = None
    initial_qc: Optional[str] = None
    library_qc: Optional[str] = None
    prep_method: Optional[str] = None
    application: Optional[str] = None
    bait_set: Optional[str] = None
    capture_kit: Optional[str] = None
    comment: Optional[str] = None
    concentration: Optional[float] = None
    concentration_sample: Optional[float] = None
    customer: Optional[str] = None
    data_analysis: Optional[str] = None
    data_delivery: Optional[str] = None
    elution_buffer: Optional[str] = None
    extraction_method: Optional[str] = None
    family_name: Optional[str] = None
    formalin_fixation_time: Optional[float] = None
    index: Optional[str] = None
    index_number: Optional[str] = None
    lab_code: Optional[str] = None
    organism: Optional[str] = None
    organism_other: Optional[str] = None
    original_lab: Optional[str] = None
    original_lab_address: Optional[str] = None
    pool: Optional[str] = None
    post_formalin_fixation_time: Optional[float] = None
    pre_processing_method: Optional[str] = None
    priority: Optional[str] = None
    quantity: Optional[str] = None
    reference_genome: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    require_qcok: Optional[str] = None
    rml_plate_name: Optional[str] = None
    selection_criteria: Optional[str] = None
    sequencing_qc_pass: Optional[str] = None
    sex: Optional[str] = None
    source: Optional[str] = None
    target_reads: Optional[float] = None
    tissue_block_size: Optional[str] = None
    tumour: Optional[str] = None
    tumour_purity: Optional[int] = None
    verified_organism: Optional[str] = None
    volume: Optional[float] = None
    well_position_rml: Optional[str] = None

    @validator("id", always=True)
    def set_id(cls, v, values: dict) -> str:
        """sett _id to prep_id"""

        return values.get("sample_id")

    class Config:
        populate_by_name = True
