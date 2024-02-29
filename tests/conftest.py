from arnold.adapter import ArnoldAdapter
from arnold.api.api_v1.api import app
from arnold.models.database import Step, LimsSample
import pytest
from mongomock import MongoClient
from fastapi.testclient import TestClient

from arnold.models.database.flow_cell import FlowCell
from arnold.settings import get_arnold_adapter

DATABASE = "testdb"


@pytest.fixture()
def mock_adapter() -> ArnoldAdapter:
    """Return a mock adapter for testing."""
    mongo_client = MongoClient()
    database = mongo_client[DATABASE]
    return ArnoldAdapter(database.client, db_name=DATABASE)


def override_arnold_adapter() -> ArnoldAdapter:
    """Function for overriding the arnold adapter dependency"""
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
def valid_samples_dict() -> list[dict]:
    return [
        LimsSample(sample_id="some_sample_id", id="some_id").model_dump(),
        LimsSample(sample_id="some_other_sample_id", id="some_other_id").model_dump(),
    ]


@pytest.fixture(scope="function")
def valid_samples() -> list[LimsSample]:
    return [
        LimsSample(sample_id="some_sample_id", id="some_id"),
        LimsSample(sample_id="some_other_sample_id", id="some_other_id"),
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


@pytest.fixture()
def valid_flow_cell_dict() -> dict:
    return {
        "instrument": "Instrument123",
        "date": "2023-12-07T08:30:00",
        "done": True,
        "buffer_expiration_date": "2023-12-15T12:00:00",
        "buffer_lot_number": "BufferLot123",
        "buffer_part_number": "BufferPart456",
        "buffer_serial_barcode": "BufferBarcode789",
        "flow_cell_expiration_date": "2023-12-20T15:45:00",
        "flow_cell_id": "FlowCellID001",
        "flow_cell_lot_number": "FlowCellLot789",
        "flow_cell_mode": "Normal",
        "flow_cell_part_number": "FlowCellPart555",
        "pe_cycle_kit": "PECycleKit123",
        "pe_expiration_date": "2023-12-25T18:30:00",
        "pe_lot_number": "PELot456",
        "pe_part_number": "PEPart789",
        "pe_serial_barcode": "PEBarcode001",
        "run_id": "RunID789",
        "sbs_cycle_kit": "SBSCycleKit555",
        "sbs_expiration_date": "2023-12-30T21:15:00",
        "sbs_lot_number": "SBSLot789",
        "sbs_part_number": "SBSPart123",
        "sbs_serial_barcode": "SBSBarcode555",
        "lanes": [
            {
                "name": "lane_1",
                "sample_id": "Sample001",
                "sample_type": "DNA",
                "barcode": "Barcode123",
            },
            {
                "name": "lane_2",
                "sample_id": "Sample002",
                "sample_type": "RNA",
                "barcode": "Barcode456",
            },
        ],
    }


@pytest.fixture()
def valid_flow_cell(valid_flow_cell_dict) -> FlowCell:
    return FlowCell.model_validate(valid_flow_cell_dict)


@pytest.fixture
def alignment_summary_metrics() -> dict:
    return {
        "category": "Sample1",
        "total_reads": 1000000.0,
        "pf_reads": 950000.0,
        "pct_pf_reads": 95.0,
        "pf_noise_reads": 5000.0,
        "pf_reads_aligned": 900000.0,
        "pct_pf_reads_aligned": 90.0,
        "pf_aligned_bases": 700000000.0,
        "pf_hq_aligned_reads": 800000.0,
        "pf_hq_aligned_bases": 600000000.0,
        "pf_hq_aligned_q20_bases": 550000000.0,
        "pf_hq_median_mismatches": 2.0,
        "pf_mismatch_rate": 0.2,
        "pf_hq_error_rate": 0.1,
        "pf_indel_rate": 0.05,
        "mean_read_length": 150.0,
        "sd_read_length": 10.0,
        "median_read_length": 145.0,
        "mad_read_length": 5.0,
        "min_read_length": 120.0,
        "max_read_length": 200.0,
        "reads_aligned_in_pairs": 850000.0,
        "pct_reads_aligned_in_pairs": 85.0,
        "pf_reads_improper_pairs": 50000.0,
        "pct_pf_reads_improper_pairs": 5.0,
        "strand_balance": 0.95,
        "pct_chimeras": 1.0,
        "pct_adapter": 2.0,
        "pct_softclip": 0.5,
        "pct_hardclip": 0.2,
        "avg_pos_3prime_softclip_length": 3.0,
    }


@pytest.fixture
def picard_duplicates() -> dict:
    return {
        "unpaired_reads_examined": 10000.0,
        "read_pairs_examined": 5000.0,
        "secondary_or_supplementary_reads": 200.0,
        "unmapped_reads": 300.0,
        "unpaired_read_duplicates": 50.0,
        "read_pair_duplicates": 30.0,
        "read_pair_optical_duplicates": 5.0,
        "percent_duplication": 0.5,
        "estimated_library_size": 15000.0,
    }


@pytest.fixture()
def hs_metrics() -> dict:
    return {
        "bait_set": "CustomBaitSet",
        "bait_territory": 300000.0,
        "bait_design_efficiency": 0.95,
        "on_bait_bases": 250000.0,
        "near_bait_bases": 20000.0,
        "off_bait_bases": 30000.0,
        "pct_selected_bases": 75.0,
        "pct_off_bait": 25.0,
        "on_bait_vs_selected": 1.2,
        "mean_bait_coverage": 150.0,
        "pct_usable_bases_on_bait": 90.0,
        "pct_usable_bases_on_target": 85.0,
        "fold_enrichment": 50.0,
        "hs_library_size": 500000.0,
        "hs_penalty_10x": 5.0,
        "hs_penalty_20x": 10.0,
        "hs_penalty_30x": 15.0,
        "hs_penalty_40x": 20.0,
        "hs_penalty_50x": 25.0,
        "hs_penalty_100x": 30.0,
        "target_territory": 280000.0,
        "genome_size": 3000000000.0,
        "total_reads": 1000000.0,
        "pf_reads": 950000.0,
        "pf_bases": 750000000.0,
        "pf_unique_reads": 800000.0,
        "pf_uq_reads_aligned": 700000.0,
        "pf_bases_aligned": 600000000.0,
        "pf_uq_bases_aligned": 500000000.0,
        "on_target_bases": 550000000.0,
        "pct_pf_reads": 95.0,
        "pct_pf_uq_reads": 85.0,
        "pct_pf_uq_reads_aligned": 75.0,
        "mean_target_coverage": 120.0,
        "median_target_coverage": 110.0,
        "max_target_coverage": 200.0,
        "min_target_coverage": 80.0,
        "zero_cvg_targets_pct": 5.0,
        "pct_exc_dupe": 1.0,
        "pct_exc_adapter": 2.0,
        "pct_exc_mapq": 3.0,
        "pct_exc_baseq": 1.5,
        "pct_exc_overlap": 0.5,
        "pct_exc_off_target": 4.0,
        "fold_80_base_penalty": 1.2,
        "pct_target_bases_1x": 100.0,
        "pct_target_bases_2x": 98.0,
        "pct_target_bases_10x": 90.0,
        "pct_target_bases_20x": 85.0,
        "pct_target_bases_30x": 80.0,
        "pct_target_bases_40x": 75.0,
        "pct_target_bases_50x": 70.0,
        "pct_target_bases_100x": 60.0,
        "pct_target_bases_250x": 50.0,
        "pct_target_bases_500x": 40.0,
        "pct_target_bases_1000x": 30.0,
        "pct_target_bases_2500x": 20.0,
        "pct_target_bases_5000x": 10.0,
        "pct_target_bases_10000x": 5.0,
        "pct_target_bases_25000x": 2.0,
        "pct_target_bases_50000x": 1.0,
        "pct_target_bases_100000x": 0.5,
        "at_dropout": 0.1,
        "gc_dropout": 0.2,
        "het_snp_sensitivity": 0.95,
        "het_snp_q": 30.0,
    }


@pytest.fixture
def insert_size() -> dict:
    return {
        "median_insert_size": 200.0,
        "mode_insert_size": 180.0,
        "median_absolute_deviation": 20.0,
        "min_insert_size": 150.0,
        "max_insert_size": 250.0,
        "mean_insert_size": 200.0,
        "standard_deviation": 15.0,
        "read_pairs": 5000.0,
        "pair_orientation": "FR",
        "width_of_10_percent": 190.0,
        "width_of_20_percent": 195.0,
        "width_of_30_percent": 200.0,
        "width_of_40_percent": 205.0,
        "width_of_50_percent": 210.0,
        "width_of_60_percent": 215.0,
        "width_of_70_percent": 220.0,
        "width_of_80_percent": 225.0,
        "width_of_90_percent": 230.0,
        "width_of_95_percent": 235.0,
        "width_of_99_percent": 240.0,
    }


@pytest.fixture
def samtools_stats() -> dict:
    return {
        "raw_total_sequences": 1000000.0,
        "filtered_sequences": 950000.0,
        "sequences": 900000.0,
        "is_sorted": 1.0,
        "first_fragments": 450000.0,
        "last_fragments": 450000.0,
        "reads_mapped": 800000.0,
        "reads_mapped_and_paired": 750000.0,
        "reads_unmapped": 100000.0,
        "reads_properly_paired": 700000.0,
        "reads_paired": 750000.0,
        "reads_duplicated": 50000.0,
        "reads_MQ0": 20000.0,
        "reads_QC_failed": 10000.0,
        "non_primary_alignments": 5000.0,
        "supplementary_alignments": 2000.0,
        "total_length": 150000000.0,
        "total_first_fragment_length": 75000000.0,
        "total_last_fragment_length": 75000000.0,
        "bases_mapped": 120000000.0,
        "bases_trimmed": 5000000.0,
        "bases_duplicated": 2500000.0,
        "mismatches": 100000.0,
        "error_rate": 0.1,
        "average_length": 150.0,
        "average_first_fragment_length": 150.0,
        "average_last_fragment_length": 150.0,
        "maximum_length": 200.0,
        "maximum_first_fragment_length": 200.0,
        "maximum_last_fragment_length": 200.0,
        "average_quality": 30.0,
        "insert_size_average": 300.0,
        "insert_size_standard_deviation": 50.0,
        "inward_oriented_pairs": 70000.0,
        "outward_oriented_pairs": 5000.0,
        "pairs_with_other_orientation": 2000.0,
        "pairs_on_different_chromosomes": 1000.0,
        "percentage_of_properly_paired_reads": 70.0,
        "reads_mapped_percent": 80.0,
        "reads_mapped_and_paired_percent": 75.0,
        "reads_unmapped_percent": 10.0,
        "reads_properly_paired_percent": 70.0,
        "reads_paired_percent": 75.0,
        "reads_duplicated_percent": 5.0,
        "reads_MQ0_percent": 2.0,
        "reads_QC_failed_percent": 1.0,
    }


@pytest.fixture
def fastp() -> dict:
    return {
        "before_filtering": {
            "total_reads": 100000,
            "total_bases": 50000000,
            "q20_bases": 48000000,
            "q30_bases": 45000000,
            "q20_rate": 0.96,
            "q30_rate": 0.90,
            "read1_mean_length": 150,
            "read2_mean_length": 150,
            "gc_content": 0.45,
        },
        "after_filtering": {
            "total_reads": 90000,
            "total_bases": 45000000,
            "q20_bases": 43000000,
            "q30_bases": 40000000,
            "q20_rate": 0.95,
            "q30_rate": 0.88,
            "read1_mean_length": 145,
            "read2_mean_length": 145,
            "gc_content": 0.43,
        },
    }


@pytest.fixture
def somalier() -> dict:
    return {
        "individual": [
            {
                "family_id": "F1",
                "paternal_id": 1001.0,
                "maternal_id": 1002.0,
                "sex": 1.0,
                "phenotype": 0.0,
                "original_pedigree_sex": 1.0,
                "gt_depth_mean": 30.0,
                "gt_depth_sd": 5.0,
                "depth_mean": 35.0,
                "depth_sd": 8.0,
                "ab_mean": 0.2,
                "ab_std": 0.05,
                "n_hom_ref": 1200.0,
                "n_het": 300.0,
                "n_hom_alt": 50.0,
                "n_unknown": 5.0,
                "p_middling_ab": 0.1,
                "X_depth_mean": 20.0,
                "X_n": 200.0,
                "X_hom_ref": 100.0,
                "X_het": 80.0,
                "X_hom_alt": 20.0,
                "Y_depth_mean": 5.0,
                "Y_n": 50.0,
            },
            {
                "family_id": "F2",
                "paternal_id": 2001.0,
                "maternal_id": 2002.0,
                "sex": 2.0,
                "phenotype": 1.0,
                "original_pedigree_sex": 2.0,
                "gt_depth_mean": 25.0,
                "gt_depth_sd": 4.0,
                "depth_mean": 30.0,
                "depth_sd": 6.0,
                "ab_mean": 0.25,
                "ab_std": 0.06,
                "n_hom_ref": 1100.0,
                "n_het": 320.0,
                "n_hom_alt": 45.0,
                "n_unknown": 8.0,
                "p_middling_ab": 0.12,
                "X_depth_mean": 18.0,
                "X_n": 180.0,
                "X_hom_ref": 90.0,
                "X_het": 70.0,
                "X_hom_alt": 20.0,
                "Y_depth_mean": 4.0,
                "Y_n": 45.0,
            },
        ],
        "comparison": {
            "relatedness": 0.8,
            "ibs0": 0.1,
            "ibs2": 0.05,
            "hom_concordance": 0.9,
            "hets_a": 250.0,
            "hets_b": 270.0,
            "hets_ab": 50.0,
            "shared_hets": 30.0,
            "hom_alts_a": 40.0,
            "hom_alts_b": 35.0,
            "shared_hom_alts": 15.0,
            "n": 2.0,
            "x_ibs0": 0.2,
            "x_ibs2": 0.1,
            "expected_relatedness": 0.75,
        },
    }


@pytest.fixture
def balsamic_case_json(
    alignment_summary_metrics: dict,
    picard_duplicates: dict,
    hs_metrics: dict,
    insert_size: dict,
    samtools_stats: dict,
    fastp: dict,
    somalier: dict,
) -> dict:
    """Return a json for the case model of the balsamic pipeline."""
    return {
        "id": "your_case_id",
        "case_info": {
            "samples": [
                {
                    "sample_id": "sample1",
                    "alignment_summary_metrics": alignment_summary_metrics,
                    "duplicates": picard_duplicates,
                    "wgs_metrics": None,
                    "hs_metrics": hs_metrics,
                    "insert_size": insert_size,
                    "samtools_stats": samtools_stats,
                    "fastp": fastp,
                },
            ],
            "somalier": somalier,
            "workflow": {
                "workflow": "balsamic",
                "version": "1",
            },
        },
    }
