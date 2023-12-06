"""Tests for the case model."""
import pytest
from _pytest.fixtures import FixtureRequest
from arnold.models.database.case import Case
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


@pytest.mark.parametrize(
    "pipeline_case_json, metric",
    [
        ("balsamic_case_json", BalsamicQCMetric),
        ("mip_dna_case_json", MIPDNAQCMetrics),
        ("mip_rna_case_json", MIPRNAQCMetrics),
        ("fluffy_case_json", FluffyQCMetrics),
        ("mutant_case_json", MutantQCMetrics),
        ("rna_fusion_case_json", RNAFusionQCMetrics),
        ("microsalt_case_json", MicroSALTQCMetrics),
        ("taxprofiler_case_json", TaxprofilerQCMetrics),
    ],
)
def test_case_model(
    pipeline_case_json: str,
    metric: type[
        BalsamicQCMetric
        | MIPDNAQCMetrics
        | MIPRNAQCMetrics
        | FluffyQCMetrics
        | MutantQCMetrics
        | RNAFusionQCMetrics
        | MicroSALTQCMetrics
        | TaxprofilerQCMetrics
    ],
    request: FixtureRequest,
):
    """Test case initialisations with different pipeline metrics."""
    # GIVEN metrics for cases from different pipelines

    # WHEN making a case model
    case: Case = Case.model_validate(request.getfixturevalue(pipeline_case_json))

    # THEN a case is made
    assert case
    assert isinstance(case.samples[0].pipeline_qc_metrics, metric)
