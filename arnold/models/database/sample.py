from typing import Optional
from pydantic import Field, BaseModel, validator
from datetime import datetime


class Sample(BaseModel):
    """LIMS Sample Collection"""

    sample_id: str
    id: Optional[str] = Field(..., alias="_id")
    ticket: Optional[str]
    received_date: Optional[datetime]
    delivery_date: Optional[datetime]
    sequenced_date: Optional[datetime]
    prepared_date: Optional[datetime]
    collection_date: Optional[datetime]
    category: Optional[str]
    sequenced_to_delivered: Optional[int]
    prepped_to_sequenced: Optional[int]
    received_to_prepped: Optional[int]
    received_to_delivered: Optional[int]
    initial_qc: Optional[str]
    library_qc: Optional[str]
    prep_method: Optional[str]
    application: Optional[str]
    bait_set: Optional[str]
    capture_kit: Optional[str]
    comment: Optional[str]
    concentration: Optional[float]
    concentration_sample: Optional[float]
    customer: Optional[str]
    data_analysis: Optional[str]
    data_delivery: Optional[str]
    elution_buffer: Optional[str]
    extraction_method: Optional[str]
    family_name: Optional[str]
    formalin_fixation_time: Optional[float]
    index: Optional[str]
    index_number: Optional[str]
    lab_code: Optional[str]
    organism: Optional[str]
    organism_other: Optional[str]
    original_lab: Optional[str]
    original_lab_address: Optional[str]
    pool: Optional[str]
    post_formalin_fixation_time: Optional[float]
    pre_processing_method: Optional[str]
    priority: Optional[str]
    quantity: Optional[str]
    reference_genome: Optional[str]
    region: Optional[str]
    region_code: Optional[str]
    require_qcok: Optional[str]
    rml_plate_name: Optional[str]
    selection_criteria: Optional[str]
    sequencing_qc_pass: Optional[str]
    sex: Optional[str]
    source: Optional[str]
    target_reads: Optional[float]
    tissue_block_size: Optional[str]
    tumour: Optional[str]
    tumour_purity: Optional[int]
    verified_organism: Optional[str]
    volume: Optional[float]
    well_position_rml: Optional[str]

    @validator("id", always=True)
    def set_id(cls, v, values: dict) -> str:
        """sett _id to prep_id"""

        return values.get("sample_id")

    class Config:
        allow_population_by_field_name = True
