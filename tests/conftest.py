from arnold.adapter import ArnoldAdapter
from arnold.api.api_v1.api import app
from arnold.models.database import Step, LimsSample
import pytest
from mongomock import MongoClient
from fastapi.testclient import TestClient

from arnold.settings import get_arnold_adapter

DATABASE = "testdb"


def override_arnold_adapter() -> ArnoldAdapter:
    """Function for overriding the arnold adapter dependency"""
    mongo_client = MongoClient()
    database = mongo_client[DATABASE]
    return ArnoldAdapter(database.client, db_name=DATABASE)


@pytest.fixture()
def mock_adapter() -> ArnoldAdapter:
    """Return a mock adapter for testing."""
    mongo_client = MongoClient()
    database = mongo_client[DATABASE]
    return ArnoldAdapter(database.client, db_name=DATABASE)


@pytest.fixture()
def fast_app_client() -> TestClient:
    """Return a mock fastapi app"""

    client = TestClient(app)
    app.dependency_overrides[get_arnold_adapter] = override_arnold_adapter
    return client


@pytest.fixture(scope="function")
def valid_step() -> Step:
    return Step(
        _id="ADM1851A3_24-125834_aliquot_samples_for_covaris",
        prep_id="ADM1851A3_24-125834",
        step_type="end_repair",
        sample_id="ADM1851A3",
        workflow="WGS",
        lims_step_name="End repair Size selection A-tailing and Adapter ligation (TruSeq PCR-free)",
        step_id="ADM1851A3_24-125834_end_repair",
        well_position="C:1",
        artifact_name="wgs3 (qPCR)",
        container_name="test",
        container_id="27-85769",
        container_type="96 well plate",
        index_name="C01 - UDI0003",
        artifact_udfs={
            "finished_library_concentration": 12,
            "finished_library_concentration_nm": 52.2170488665,
            "finished_library_size": 350,
        },
        process_udfs={
            "pcr_instrument_incubation": "Polo",
            "library_preparation_method": "1464",
        },
    )


@pytest.fixture(scope="function")
def valid_sample() -> LimsSample:
    return LimsSample(sample_id="some_sample_id", id="some_id")


@pytest.fixture(scope="function")
def valid_samples() -> list[dict]:
    return [
        LimsSample(sample_id="some_sample_id", id="some_id").model_dump(),
        LimsSample(sample_id="some_other_sample_id", id="some_other_id").model_dump(),
    ]


@pytest.fixture(scope="function")
def invalid_samples() -> list[dict]:
    return [
        dict(id="some_id"),
        dict(sample_id="some_other_sample_id", id="some_other_id"),
    ]


@pytest.fixture(scope="function")
def invalid_sample() -> dict:
    return dict(sample_id="some_sample_id")


@pytest.fixture(scope="function")
def invalid_step() -> dict:
    return dict(
        step_type="end_repair",
        sample_id="ADM1851A3",
        workflow="WGS",
        lims_step_name="End repair Size selection A-tailing and Adapter ligation (TruSeq PCR-free)",
        step_id="ADM1851A3_24-125834_end_repair",
        well_position="C:1",
        artifact_name="wgs3 (qPCR)",
        container_name="test",
        container_id="27-85769",
    )


@pytest.fixture
def balsamic_case_json() -> dict:
    """Return a json for the case model of the balsamic pipeline."""
    return {
        "id": "subsonichedgehog",
        "pipeline": {"name": "Balsamic", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "pct_pf_reads_improper_pairs": 45.5,
                    "mean_insert_size": 73,
                    "median_coverage": 58,
                    "pct_15x": 24.8,
                    "pct_30x": 62.1,
                    "pct_60x": 87.3,
                    "pct_100x": 9.2,
                    "fold_80_base_penalty": 10.1,
                    "pct_duplication": 10.5,
                    "pct_read1_duplication": 33.7,
                    "pct_read2_dulpication": 15.4,
                    "number_of_sites_snvs": 42,
                    "number_of_sites_svs": 69,
                    "relatedness": 91.6,
                    "pct_off_bait": 37.2,
                    "mean_target_coverage": 54.9,
                    "median_target_coverage": 62.3,
                    "pct_target_bases_20x": 18.7,
                    "pct_target_bases_50x": 51.2,
                    "pct_target_bases_100x": 87.9,
                    "pct_target_bases_250x": 33.5,
                    "pct_target_bases_500x": 5.6,
                    "pct_target_bases_1000x": 1.9,
                    "gc_dropout": 64.4,
                },
            }
        ],
    }


@pytest.fixture
def mip_dna_case_json() -> dict:
    """Return a json for the case model of the mip-dna pipeline."""
    return {
        "id": "supersonichedgehog",
        "pipeline": {"name": "mip-dna", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "gc_dropout": 55.5,
                    "at_dropout": 12.3,
                    "total_reads": 10000,
                    "reads_mapped": 9000,
                    "pct_reads_mapped": 90.0,
                    "mean_insert_size": 300,
                    "fraction_duplicate": 10.5,
                    "gender": "Male",
                    "pct_target_bases_10x": 95.5,
                    "pct_target_bases_20x": 90.5,
                    "pct_off_bait": 5.2,
                    "mean_target_coverage": 120.8,
                    "median_target_coverage": 118.2,
                    "fold_80_base_penalty": 2.7,
                    "pct_adapter": 3.6,
                },
            }
        ],
    }


@pytest.fixture
def mip_rna_case_json() -> dict:
    return {
        "id": "subsonicturtle",
        "pipeline": {"name": "mip-rna", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "fraction_duplicates": 5.0,
                    "pct_intergenic_bases": 10.2,
                    "pct_mrna_bases": 75.5,
                    "pct_uniquely_mapped_reads": 85.0,
                    "pct_adapter": 2.3,
                },
            }
        ],
    }


@pytest.fixture
def fluffy_case_json() -> dict:
    return {
        "id": "supersonicturtle",
        "pipeline": {"name": "fluffy", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "reads_mapped": 9500.0,
                    "duplication_rate": 7.8,
                    "gc_dropout": 18.5,
                    "at_dropout": 5.2,
                    "bin_variance": 2.0,
                    "fetal_fraction_x": 1.2,
                    "fetal_fraction_y": 1.1,
                    "stdev_13": 0.5,
                    "stdev_18": 0.6,
                    "stdev_21": 0.7,
                },
            }
        ],
    }


@pytest.fixture
def mutant_case_json() -> dict:
    return {
        "id": "updog",
        "pipeline": {"name": "Mutant", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "negative_control_reads": 100,
                    "total_reads": 12000,
                    "trimmed_reads": 11000,
                    "pct_aligned": 90.5,
                    "mean_read_length": 150.5,
                    "median_insert_size": 180.0,
                    "median_coverage": 120.0,
                    "pct_coverage_10x": 95.0,
                    "pct_coverage_30x": 85.0,
                    "pct_coverage_50x": 75.0,
                    "pct_coverage_100x": 60.0,
                    "pct_trimmed": 10.0,
                    "pct_duplicates": 5.0,
                    "pct_gc": 45.5,
                    "pct_n_bases": 2.0,
                    "lineage_pangolin": "B.1.1.7",
                    "lineage_nextclade": "20B",
                },
            }
        ],
    }


@pytest.fixture
def rna_fusion_case_json() -> dict:
    return {
        "id": "downdog",
        "pipeline": {"name": "rna-fusion", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "pct_mrna_bases": 70.2,
                    "pct_ribosomal_bases": 5.5,
                    "pct_duplication": 8.0,
                    "pct_surviving": 90.0,
                    "pct_adapter": 2.0,
                    "read1_mean_length_after_filtering": 100,
                    "q20_rate_after_filtering": 98.5,
                    "q30_rate_after_filtering": 95.0,
                    "gc_content_after_filtering": 55.5,
                    "total_reads": 15000,
                    "bias_5_3": 0.02,
                    "reads_aligned": 14000,
                    "pct_uniquely_mapped": 92.0,
                    "percent_mapped_reads": 94.5,
                    "insert_size": 200,
                },
            }
        ],
    }


@pytest.fixture
def microsalt_case_json() -> dict:
    return {
        "id": "realparrot",
        "pipeline": {"name": "Microsalt", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "total_reads": 8000,
                    "n50": "2000",
                    "qc_percentage": 95.5,
                    "sequence_type": "WGS",
                    "pct_coverage_10x": 97.0,
                    "pct_coverage_20x": 90.0,
                    "pct_coverage_50x": 80.0,
                    "pct_coverage_100x": 70.0,
                    "pct_mapped_reads": 95.5,
                    "pct_duplicates": 5.0,
                    "insert_size": 250,
                    "avg_coverage": 120,
                },
            }
        ],
    }


@pytest.fixture
def taxprofiler_case_json():
    return {
        "id": "fakeparrot",
        "pipeline": {"name": "Taxprofiler", "version": "0.0.0"},
        "samples": [
            {
                "id": "ACC2341",
                "pipeline_qc_metrics": {
                    "total_reads": 10000,
                    "avg_read_length": 150.5,
                    "pct_duplicates": 5.0,
                    "pct_gc": 45.5,
                    "trimmed_reads": 9000,
                    "avg_trimmed_read_length": 145.5,
                    "pct_aligned": 90.0,
                    "reads_mapped": 9500,
                },
            }
        ],
    }
