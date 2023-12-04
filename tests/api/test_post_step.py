from fastapi.testclient import TestClient
from arnold.api.api_v1.endpoints.step import router
from fastapi import status

client = TestClient(router)


def test_post_valid_step(fast_app_client, valid_step):
    # GIVEN valid step request data
    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/step/", json=valid_step.dict())

    # THEN assert status is ok
    assert response.status_code == status.HTTP_200_OK


def test_post_invalid_step(fast_app_client, invalid_step):
    # GIVEN invalid step request data

    # WHEN running the user request with the data
    response = fast_app_client.post("/api/v1/step/", json=invalid_step)

    # THEN assert status 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_step_already_in_db(mocker, fast_app_client, valid_step):
    # GIVEN that the step to load is already in the database. Ie, find_step is True
    mocker.patch("arnold.crud.read.step.find_step")

    # WHEN running the step request with data
    response = fast_app_client.post("/api/v1/step/", json=valid_step.dict())

    # THEN assert status is 405
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "step already in database" in str(response.content)


def test_post_step_create_step_failing(mocker, fast_app_client, valid_step):
    # GIVEN that the step is not in the database but the create_step fails
    mocker.patch("arnold.crud.read.step.find_step", return_value=False)
    mocker.patch(
        "arnold.crud.create.create_step", side_effect=Exception("mocked error")
    )

    # WHEN running the step request with data
    response = fast_app_client.post("/api/v1/step/", json=valid_step.dict())

    # THEN assert status is 405
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "mocked error" in str(response.content)
