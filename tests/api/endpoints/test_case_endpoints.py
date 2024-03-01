"""This modules holds tests for case API endpoints."""
import pytest
from _pytest.fixtures import FixtureRequest
from fastapi import status
from fastapi.testclient import TestClient

from arnold.api.api_v1.endpoints.case import router
from arnold.models.database.case.case import Case

client = TestClient(router)


@pytest.mark.parametrize(
    "case_json_data",
    [
        "balsamic_case_json",
    ],
)
def test_create_case(
    fast_app_client: TestClient, case_json_data, request: FixtureRequest
):
    """Test to create a case in the database."""
    # GIVEN a case
    case: dict = request.getfixturevalue(case_json_data)

    # WHEN running the request
    response = fast_app_client.post("api/v1/case/", json=case)

    # THEN assert that the status is ok
    assert response.status_code == status.HTTP_201_CREATED


def test_get_case(fast_app_client: TestClient, balsamic_case_json, mocker):
    """Test to retrieve a case from the database."""
    # GIVEN a case in the database
    case: Case = Case.model_validate(balsamic_case_json)
    mocker.patch(
        "arnold.crud.read.case.get_case",
        return_value=case,
    )

    # WHEN retrieving a case from the database
    response = fast_app_client.get(f"/api/v1/case/{case.id}")

    # THEN a case is returned
    assert response.status_code == status.HTTP_200_OK
