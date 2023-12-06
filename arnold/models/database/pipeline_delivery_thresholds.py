"""This module holds the models for the pipeline delivery tresholds."""
from pydantic import BaseModel


class BalsamicDeliveryThresholds(BaseModel):
    pct_pf_reads_improper_pairs: float
    relatedness: float
    pct_15x: float
    pct_60x: float
    number_of_sites_snvs: int
    number_of_sites_svs: int
    pct_target_bases_20x: float
    pct_target_bases_250x: float
    pct_target_bases_500x_gms_myeloid: float
    pct_target_bases_500x_lymphoma: float
    pct_target_bases_1000x: float
    gc_dropout: float


class FluffyPipelineThresholds(BaseModel):
    total_reads: int


class MIPDNADeliveryThresholds(BaseModel):
    # No thresholds given yet
    pass


class MIPRNADeliveryThresholds(BaseModel):
    # No thresholds given yet
    pass


class MutantPipelineThresholds(BaseModel):
    # No thresholds given yet
    pass


class RNAFusionDeliveryThresholds(BaseModel):
    pct_mrna_bases: float
    pct_ribosomal_bases: float
    pct_duplication: float
    total_reads: int
    pct_uniquely_mapped: float


class TaxprofilerPipeLineThresholds(BaseModel):
    # None given yet
    pass
