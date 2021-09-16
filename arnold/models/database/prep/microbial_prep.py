from typing import Optional

from pydantic import BaseModel


class MicrobialPrep(BaseModel):
    sample_concentration: Optional[float]
    lot_nr_beads_buffer_exchange: Optional[str]
    lot_nr_etoh_buffer_exchange: Optional[str]
    lot_nr_h2o_buffer_exchange: Optional[str]
    buffer_exchange_method: Optional[str]
    sample_normalization_method: Optional[str]
    normalized_sample_concentration: Optional[float]
    lot_nr_dilution_buffer_sample_normalization: Optional[str]
    lot_nr_tagmentation_buffer: str
    lot_nr_tagmentation_enzyme: str
    lot_nr_index: str
    lot_nr_pcr_mix: str
    pcr_instrument_incubation: str
    pcr_instrument_amplification: str
    nr_pcr_cycles: int
    lot_nr_beads_library_prep: str
    lot_nr_etoh_library_prep: str
    lot_nr_h2o_library_prep: str
    finished_library_concentration: float
    finished_library_concentration_nm: float
    finished_library_size: Optional[float]
    finished_library_average_size: float
    lot_nr_dilution_buffer_library_normalization: Optional[str]
    normalized_library_concentration: Optional[float]
    library_normalization_method: Optional[str]

    class Config:
        allow_population_by_field_name = True
