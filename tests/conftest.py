from arnold.adapter import ArnoldAdapter
from arnold.api.api_v1.api import app
from arnold.models.database import Step, Sample
import pytest
from mongomock import MongoClient
from fastapi.testclient import TestClient

from arnold.settings import get_arnold_adapter

DATABASE = "testdb"


def override_arnold_adapter():
    """Function for overriding the arnold adapter dependency"""

    mongo_client = MongoClient()
    database = mongo_client[DATABASE]
    return ArnoldAdapter(database.client, db_name=DATABASE)


@pytest.fixture()
def fast_app_client():
    """Return a mock fastapi app"""

    client = TestClient(app)
    app.dependency_overrides[get_arnold_adapter] = override_arnold_adapter
    return client


@pytest.fixture(scope="function")
def valid_step():
    return Step(
        id="ADM1851A3_24-125834_aliquot_samples_for_covaris",
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
        process_udfs={"pcr_instrument_incubation": "Polo", "library_preparation_method": "1464"},
    )


@pytest.fixture(scope="function")
def valid_sample():
    return Sample(sample_id="some_sample_id", id="some_id")


@pytest.fixture(scope="function")
def valid_samples():
    return [
        Sample(sample_id="some_sample_id", id="some_id").dict(),
        Sample(sample_id="some_other_sample_id", id="some_other_id").dict(),
    ]


@pytest.fixture(scope="function")
def invalid_samples():
    return [
        dict(id="some_id"),
        dict(sample_id="some_other_sample_id", id="some_other_id"),
    ]


@pytest.fixture(scope="function")
def invalid_sample():
    return dict(sample_id="some_sample_id")


@pytest.fixture(scope="function")
def invalid_step():
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
