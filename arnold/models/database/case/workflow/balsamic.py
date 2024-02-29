"""Module for the workflow models."""
from pydantic import BaseModel

from arnold.models.database.case.mutliqc import (
    Somalier,
    PicardAlignmentSummary,
    PicardDuplicates,
    PicardHsMetrics,
    PicardInsertSize,
    PicardWGSMetrics,
    SamtoolsStats,
    Fastp,
)
from arnold.models.database.case.workflow.workflowinfo import WorkflowInfo


class BalsamicSample(BaseModel):
    sample_id: str
    alignment_summary_metrics: PicardAlignmentSummary | None
    duplicates: PicardDuplicates | None
    wgs_metrics: PicardWGSMetrics | None = None
    hs_metrics: PicardHsMetrics | None
    insert_size: PicardInsertSize | None
    samtools_stats: SamtoolsStats | None
    fastp: Fastp | None


class Balsamic(BaseModel):
    samples: list[BalsamicSample]
    somalier: Somalier | None
    workflow: WorkflowInfo
