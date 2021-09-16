from typing import Optional

from pydantic import Field, BaseModel


class SarsCov2Prep(BaseModel):
    sample_concentration: Optional[float]
    sample_size: Optional[float]
    lot_nr_tagmentation_beads: str
    lot_nr__stop_tagment_buffer: str
    lot_nr_index: str
    lot_nr_pcr_mix: str
    lot_nr_tagmentation_wash_buffer: str
    lot_nr_h2o_library_preparation: str
    lot_nr_TB1: str
    pcr_instrument_tagmentation: str
    pcr_instrument_amplification: str
    library_preparation_method: str
    liquid_handling_system: str
    pooling_method: str
    clean_up_method: str
    lot_nr_beads_clean_up: str
    lot_nr_etoh_clean_up: str
    lot_nr_h2o_clean_up: str
    lot_nr_resuspension_buffer_clean_up: str
    finished_library_concentration: float
    finished_library_concentration_nm: float
    finished_library_size: Optional[float]

    class Config:
        allow_population_by_field_name = True
