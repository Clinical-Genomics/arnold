from typing import Optional
from pydantic import BaseModel


class SarsCov2Prep(BaseModel):
    sample_concentration: Optional[float]
    sample_size: Optional[float]
    lot_nr_tagmentation_beads: Optional[str]
    lot_nr__stop_tagment_buffer: Optional[str]
    lot_nr_index: Optional[str]
    lot_nr_pcr_mix: Optional[str]
    lot_nr_tagmentation_wash_buffer: Optional[str]
    lot_nr_h2o_library_preparation: Optional[str]
    lot_nr_TB1: Optional[str]
    pcr_instrument_tagmentation: Optional[str]
    pcr_instrument_amplification: Optional[str]
    library_preparation_method: Optional[str]
    liquid_handling_system: Optional[str]
    pooling_method: Optional[str]
    clean_up_method: Optional[str]
    lot_nr_beads_clean_up: Optional[str]
    lot_nr_etoh_clean_up: Optional[str]
    lot_nr_h2o_clean_up: Optional[str]
    lot_nr_resuspension_buffer_clean_up: Optional[str]
    finished_library_concentration: Optional[float]
    finished_library_concentration_nm: Optional[float]
    finished_library_size: Optional[float]

    class Config:
        allow_population_by_field_name = True
