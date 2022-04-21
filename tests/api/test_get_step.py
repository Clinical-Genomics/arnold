from fastapi.testclient import TestClient
from arnold.api.api_v1.endpoints.step import router
from fastapi import status

client = TestClient(router)


def test_get_step(mocker, fast_app_client, valid_step):
    # GIVEN valid step request data
    mocker.patch("arnold.crud.read.step.find_step", return_value=valid_step)

    # WHEN running the user request with the data
    response = fast_app_client.get("/api/v1/step/some_id")

    # THEN assert status is ok
    assert response.status_code == status.HTTP_200_OK


def test_get_step_failing(mocker, fast_app_client):
    # GIVEN that the step is not in the database but the create_step fails
    mocker.patch("arnold.crud.read.step.find_step", return_value=None)

    # WHEN running the step request with data
    response = fast_app_client.get("/api/v1/step/some_id")

    # THEN assert status is 405
    assert response.status_code == status.HTTP_200_OK
