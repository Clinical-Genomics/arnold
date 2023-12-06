"""Module that holds the pipeline specific qc metrics models."""
from pydantic import BaseModel


class BalsamicQCMetric(BaseModel):
    pct_pf_reads_improper_pairs: float
    mean_insert_size: int
    median_coverage: int
    pct_15x: float
    pct_30x: float
    pct_60x: float
    pct_100x: float
    fold_80_base_penalty: float
    pct_duplication: float
    pct_read1_duplication: float
    pct_read2_dulpication: float
    number_of_sites_snvs: int
    number_of_sites_svs: int
    relatedness: float
    pct_off_bait: float
    mean_target_coverage: float
    median_target_coverage: float
    pct_target_bases_20x: float
    pct_target_bases_50x: float
    pct_target_bases_100x: float
    pct_target_bases_250x: float
    pct_target_bases_500x: float
    pct_target_bases_1000x: float
    gc_dropout: float


class FluffyQCMetrics(BaseModel):
    reads_mapped: float
    duplication_rate: float
    gc_dropout: float
    at_dropout: float
    bin_variance: float
    fetal_fraction_x: float
    fetal_fraction_y: float
    stdev_13: float
    stdev_18: float
    stdev_21: float


class MicroSALTQCMetrics(BaseModel):
    total_reads: int
    n50: str
    qc_percentage: float
    sequence_type: str
    pct_coverage_10x: float
    pct_coverage_20x: float
    pct_coverage_50x: float
    pct_coverage_100x: float
    pct_mapped_reads: float
    pct_duplicates: float
    insert_size: int
    avg_coverage: int


class MIPDNAQCMetrics(BaseModel):
    gc_dropout: float
    at_dropout: float
    total_reads: int
    reads_mapped: int
    pct_reads_mapped: float
    mean_insert_size: int
    fraction_duplicate: float
    gender: str
    pct_target_bases_10x: float
    pct_target_bases_20x: float
    pct_off_bait: float
    mean_target_coverage: float
    median_target_coverage: float
    fold_80_base_penalty: float
    pct_adapter: float


class MIPRNAQCMetrics(BaseModel):
    fraction_duplicates: float
    pct_intergenic_bases: float
    pct_mrna_bases: float
    pct_uniquely_mapped_reads: float
    pct_adapter: float


class MutantQCMetrics(BaseModel):
    negative_control_reads: int
    total_reads: int
    trimmed_reads: int
    pct_aligned: float
    mean_read_length: float
    median_insert_size: float
    median_coverage: float
    pct_coverage_10x: float
    pct_coverage_30x: float
    pct_coverage_50x: float
    pct_coverage_100x: float
    pct_trimmed: float
    pct_duplicates: float
    pct_gc: float
    pct_n_bases: float
    lineage_pangolin: str
    lineage_nextclade: str


class RNAFusionQCMetrics(BaseModel):
    pct_mrna_bases: float
    pct_ribosomal_bases: float
    pct_duplication: float
    pct_surviving: float
    pct_adapter: float
    read1_mean_length_after_filtering: int
    q20_rate_after_filtering: float
    q30_rate_after_filtering: float
    gc_content_after_filtering: float
    pct_duplication: float
    total_reads: int
    bias_5_3: float
    reads_aligned: int
    pct_uniquely_mapped: float
    percent_mapped_reads: float
    insert_size: int


class TaxprofilerQCMetrics(BaseModel):
    total_reads: int
    avg_read_length: float
    pct_duplicates: float
    pct_gc: float
    trimmed_reads: int
    avg_trimmed_read_length: float
    pct_aligned: float
    reads_mapped: int
