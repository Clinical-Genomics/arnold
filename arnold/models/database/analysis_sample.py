"""This module holds the sample model."""
from pydantic import BaseModel

from arnold.models.database.pipeline_qc_metrics import (
    BalsamicQCMetric,
    FluffyQCMetrics,
    MicroSALTQCMetrics,
    MIPDNAQCMetrics,
    MIPRNAQCMetrics,
    MutantQCMetrics,
    RNAFusionQCMetrics,
    TaxprofilerQCMetrics,
)


class AnalysisSample(BaseModel):
    id: str
    pipeline_qc_metrics: BalsamicQCMetric | MIPDNAQCMetrics | MIPRNAQCMetrics | FluffyQCMetrics | MutantQCMetrics | RNAFusionQCMetrics | MicroSALTQCMetrics | TaxprofilerQCMetrics
